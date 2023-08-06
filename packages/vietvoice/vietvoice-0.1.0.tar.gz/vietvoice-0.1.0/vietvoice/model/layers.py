import torch
import torch.nn as nn
import torch.nn.functional as F

from vietvoice.utils.mask import get_mask_from_lengths

class ConvNorm(nn.Module):
    def __init__(self, in_channels, out_channels, 
                 kernel_size, stride=1, padding=None, dilation=1, bias=True, w_init_gain='linear'):
        super(ConvNorm, self).__init__()
        
        if padding is None:
            assert kernel_size % 2 ==1
            padding = dilation*(kernel_size - 1)//2
        
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size=kernel_size, 
                              stride=stride, padding=padding, dilation=dilation, bias=bias)    
        
        
        nn.init.xavier_uniform_(self.conv.weight, gain=nn.init.calculate_gain(w_init_gain))
        
        
    def forward(self, x):
        x = self.conv(x)
        
        return x
    
class Encoder(nn.Module):
    def __init__(self, n_convolutions, kernel_size, embedding_dim):
        super(Encoder, self).__init__()
        
        assert embedding_dim % 2 == 0
        
        self.convolutions = nn.ModuleList()
        for _ in range(n_convolutions):
            conv_norm = ConvNorm(embedding_dim, embedding_dim,
                                kernel_size = kernel_size, stride=1,
                                padding = (kernel_size -1) //2,
                                dilation=1, w_init_gain='relu'
                                )
            
            batch_norm = nn.BatchNorm1d(embedding_dim)
            
            conv_layer = nn.Sequential(
                conv_norm,
                batch_norm                
            )
            
            self.convolutions.append(conv_layer)
        
        self.lstm = nn.LSTM(embedding_dim, embedding_dim//2, 1, batch_first=True, bidirectional=True)
        
    
    def forward(self, x, input_lengths):
        """
        x: BxHxT
        """
        
        for conv in self.convolutions:
            x = F.dropout(F.relu(conv(x)), 0.5, self.training)
        
        x = x.transpose(1, 2)
        
        input_lengths = input_lengths.cpu().numpy()
        
        x = nn.utils.rnn.pack_padded_sequence(x, input_lengths, batch_first=True)
        
        outputs, _ = self.lstm(x)
        
        outputs, _ = nn.utils.rnn.pad_packed_sequence(outputs, batch_first=True)
        
        return outputs
        
    def inference(self, x):
        for conv in self.convolutions:
            x = F.dropout(F.relu(conv(x)), 0.5, self.training)
    
        x = x.transpose(1, 2)
        
        outputs, _ = self.lstm(x)

        return outputs

class LinearNorm(nn.Module):
    def __init__(self, in_dim, out_dim, bias=True, w_init_gain='linear'):
        super(LinearNorm, self).__init__()
        
        self.linear_layer = nn.Linear(in_dim, out_dim, bias=bias)
        nn.init.xavier_uniform_(self.linear_layer.weight, gain=nn.init.calculate_gain(w_init_gain))
        
    def forward(self, x):
        x = self.linear_layer(x)
        
        return x    
    
class Prenet(nn.Module):
    def __init__(self, in_dim, sizes):
        super(Prenet, self).__init__()
        in_sizes = [in_dim] + sizes[:-1]
        self.layers = nn.ModuleList()
        
        for in_size, out_size in zip(in_sizes, sizes):
            linear = LinearNorm(in_size, out_size, bias=False)
            
            self.layers.append(linear)
    
    def forward(self, x):
        for linear in self.layers:
            x = F.dropout(F.relu(linear(x)), 0.1, training=True)
        
        return x

class LocationLayer(nn.Module):
    def __init__(self, attention_n_filters, attention_kernel_size, attention_dim):
        super(LocationLayer, self).__init__()
        
        padding = (attention_kernel_size - 1)//2
        self.location_conv = ConvNorm(2, attention_n_filters, kernel_size=attention_kernel_size, padding=padding, bias=False, stride=1, dilation=1)
        
        self.location_dense = LinearNorm(attention_n_filters, attention_dim, bias=False, w_init_gain='tanh')
        
    def forward(self, attention_weights_cat):
        """
        attention_weights_cat: Bx2xT
        """
        processed_attention = self.location_conv(attention_weights_cat)
        
        processed_attention = processed_attention.transpose(1, 2)
        processed_attention = self.location_dense(processed_attention)
        
        return processed_attention
    
class Attention(nn.Module):
    def __init__(self, attention_rnn_dim, memory_dim, attention_dim,
                attention_location_n_filters, attention_location_kernel_size):
        super(Attention, self).__init__()
        
        self.query_layer = LinearNorm(attention_rnn_dim, attention_dim, bias=False, w_init_gain='tanh')
        self.memory_layer = LinearNorm(memory_dim, attention_dim, bias=False, w_init_gain='tanh')
        self.v = LinearNorm(attention_dim, 1, bias=False)
        
        self.location_layer = LocationLayer(attention_location_n_filters, attention_location_kernel_size, attention_dim)
        
        self.score_mask_value = -float('inf')
        
    def get_alignment_energies(self, query, processed_memory, attention_weights_cat):
        """
        query: BxAttention_rnn_dim
        process_memory: BxTxAttention_dim
        attention_weights_cat: cumulative and prev. att weights (B, 2, max_time)
        """
        
        query = query.unsqueeze(1)
        processed_query = self.query_layer(query)
        
        processed_attention_weights = self.location_layer(attention_weights_cat)
        
        energies = torch.tanh(processed_query + processed_attention_weights + processed_memory)
        energies = self.v(energies)
        energies = energies.squeeze(-1)
        
        return energies
    
    def forward(self, attention_hidden_state, memory, processed_memory, attention_weights_cat, mask):
        
        alignment = self.get_alignment_energies(attention_hidden_state, processed_memory, attention_weights_cat)
        
        if mask is not None:
            alignment.masked_fill_(mask, self.score_mask_value)
        
        
        attention_weights = F.softmax(alignment, dim=1)
        attention_context = torch.bmm(attention_weights.unsqueeze(1), memory)
        attention_context = attention_context.squeeze(1)
        
        return attention_context, attention_weights
    
class Decoder(nn.Module):
    def __init__(self, n_mel_channels, encoder_embedding_dim, 
                 attention_rnn_dim, decoder_rnn_dim, prenet_dim, 
                 max_decoder_steps, gate_threshold, 
                 p_attention_dropout, p_decoder_dropout, attention_config):
        super(Decoder, self).__init__()
        self.n_mel_channels = n_mel_channels
        self.encoder_embedding_dim = encoder_embedding_dim
        self.attention_rnn_dim = attention_rnn_dim
        self.decoder_rnn_dim = decoder_rnn_dim
        
        self.max_decoder_steps = max_decoder_steps
        self.gate_threshold = gate_threshold
        
        self.p_attention_dropout = p_attention_dropout
        self.p_decoder_dropout = p_decoder_dropout
        
        self.prenet = Prenet(n_mel_channels, [prenet_dim, prenet_dim])
        
        self.attention_rnn = nn.LSTMCell(prenet_dim + encoder_embedding_dim, attention_rnn_dim)
        
        self.attention_layer = Attention(attention_rnn_dim, encoder_embedding_dim, **attention_config)
        
        self.decoder_rnn = nn.LSTMCell(attention_rnn_dim + encoder_embedding_dim, decoder_rnn_dim)
        
        self.linear_projection = LinearNorm(decoder_rnn_dim + encoder_embedding_dim, n_mel_channels)
        
        self.gate_layer = LinearNorm(attention_rnn_dim + encoder_embedding_dim, 1, bias=True, w_init_gain='sigmoid')
    
    def get_go_frame(self, memory):
        batch_size = memory.size(0)
        
        decoder_input = memory.new(batch_size, self.n_mel_channels).zero_()
        return decoder_input
    
    def initialize_decoder_states(self, memory, mask):
        batch_size = memory.size(0)
        max_time = memory.size(1)
        
        # init state for first rnn
        self.attention_hidden = memory.new(batch_size, self.attention_rnn_dim).zero_()
        self.attention_cell = memory.new(batch_size, self.attention_rnn_dim).zero_()
        
        # init state for second rnn
        self.decoder_hidden = memory.new(batch_size, self.decoder_rnn_dim).zero_()
        self.decoder_cell = memory.new(batch_size, self.decoder_rnn_dim).zero_()
        
        # init attention
        self.attention_weights = memory.new(batch_size, max_time).zero_()
        self.attention_weights_cum = memory.new(batch_size, max_time).zero_()
        self.attention_context = memory.new(batch_size, self.encoder_embedding_dim).zero_()
        
        # save memory
        self.memory = memory
        self.processed_memory = self.attention_layer.memory_layer(memory)
        self.mask = mask
    
    
    def transform_decoder_outputs(self, mel_outputs, gate_outputs, alignments):

        # (T_out, B, n_mel_channels) -> # (B, n_mel_channels, T_out)
        mel_outputs = torch.stack(mel_outputs).permute(1, 2, 0)
        
        # (T_out, B) -> (B, T_out)
        gate_outputs = torch.stack(gate_outputs).transpose(0, 1)
         # (T_out, B, T_in) -> (B, T_out, T_in)
        alignments = torch.stack(alignments).transpose(0, 1)

        
        return mel_outputs, gate_outputs, alignments
    
    def decode(self, decoder_input):
        """
        decoder_input: previous mel output
        """
        
        # first rnn use attention_context of previous timestep
        cell_input = torch.cat((decoder_input, self.attention_context), dim=1)
        self.attention_hidden, self.attention_cell = self.attention_rnn(cell_input, 
                                                        (self.attention_hidden, self.attention_cell))
        
        self.attention_hidden = F.dropout(self.attention_hidden, self.p_attention_dropout, training=self.training)
        
        attention_weights_cat = torch.cat((
            self.attention_weights.unsqueeze(1), 
            self.attention_weights_cum.unsqueeze(1)),
            dim=1)
        
        # compute attention_context of current step
        self.attention_context, self.attention_weights = self.attention_layer(self.attention_hidden, self.memory, self.processed_memory, attention_weights_cat, self.mask)
        
        self.attention_weights_cum += self.attention_weights
        
        # second rnn
        decoder_input = torch.cat((self.attention_hidden, self.attention_context), dim=1)
        
        self.decoder_hidden, self.decoder_cell = self.decoder_rnn(decoder_input, 
                                                                  (self.decoder_hidden, self.decoder_cell))
        
        self.decoder_hidden = F.dropout(self.decoder_hidden, self.p_decoder_dropout, training=self.training)
        
        
        # linear projection 
        decoder_hidden_attention_context = torch.cat((self.decoder_hidden, self.attention_context), dim=1)
        
        decoder_output = self.linear_projection(decoder_hidden_attention_context)
        
        # gate prediction
        gate_prediction = self.gate_layer(decoder_hidden_attention_context)
        
        return decoder_output, gate_prediction, self.attention_weights
    
    def forward(self, memory, decoder_inputs, memory_lengths):
        """
        memory: encoder outputs
        decoder_inputs: decoder inputs for teaching force. i.e. mel-specs: BxHxT
        memory_lengths: encoder output lengths for attention masking.
        """
        # add init frame to decoder_inputs
        init_frame = self.get_go_frame(memory).unsqueeze(0) # 1xBxH
        decoder_inputs = decoder_inputs.permute(2, 0, 1) # TxBxH
        decoder_inputs = torch.cat((init_frame, decoder_inputs), dim=0)
        
        decoder_inputs = self.prenet(decoder_inputs)
        
        self.initialize_decoder_states(memory, mask= ~get_mask_from_lengths(memory_lengths))
        
        mel_outputs, gate_outputs, alignments = [], [], []        
        max_time = decoder_inputs.size(0) - 1
        
        for t in range(max_time):
            decoder_input = decoder_inputs[t]
            
            mel_output, gate_output, attention_weights = self.decode(decoder_input)            
                            
            mel_outputs.append(mel_output)
            gate_outputs.append(gate_output.squeeze(1))
            alignments.append(attention_weights)
            
        outputs = self.transform_decoder_outputs(mel_outputs, gate_outputs, alignments)
        
        return outputs
    
    def inference(self, memory):
        """
        memory: BxTxH
        """
        
        decoder_input = self.get_go_frame(memory)
        self.initialize_decoder_states(memory, mask=None)
        
        mel_outputs, gate_outputs, alignments = [], [], []
        
        while True:
            decoder_input = self.prenet(decoder_input)
            
            mel_output, gate_output, alignment = self.decode(decoder_input)
            mel_outputs.append(mel_output)
            gate_outputs.append(gate_output.squeeze(1))
            alignments.append(alignment)
            
            if torch.sigmoid(gate_output) > self.gate_threshold:
                break
            elif len(mel_outputs) >= self.max_decoder_steps:
                print("Warning! Reached max decoder steps")
                break
            
            decoder_input = mel_output
        
        outputs = self.transform_decoder_outputs(mel_outputs, gate_outputs, alignments)
        
        return outputs

class Postnet(nn.Module):
    def __init__(self, n_convolutions, n_mel_channels, embedding_dim, kernel_size): 
        super(Postnet, self).__init__()
        
        self.convolutions = nn.ModuleList()
        
        sizes = [n_mel_channels] + [embedding_dim]*(n_convolutions - 1) + [n_mel_channels]
        activations = ['tanh']*4 + ['linear']
        
        # output_size of previous conv is input_size of next layer
        for i in range(n_convolutions):
            padding = (kernel_size - 1)//2
            conv_norm = ConvNorm(sizes[i], sizes[i+1], kernel_size=kernel_size, padding=padding, stride=1, dilation=1, w_init_gain=activations[i])
            
            conv = nn.Sequential(
                conv_norm,
                nn.BatchNorm1d(sizes[i+1])
            )
            
            self.convolutions.append(conv)
    
    def forward(self, x):
        for i in range(len(self.convolutions) - 1):
            x = F.dropout(torch.tanh(self.convolutions[i](x)), 0.5, training=self.training)
        
        x = F.dropout(self.convolutions[-1](x), 0.5, training=self.training)
        
        return x            
