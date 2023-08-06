vietnamese_phoneme = ['ɯəj', 'ɤ̆j', 'ʷiə', 'ɤ̆w', 'ɯəw', 'ʷet', 'iəw', 'uəj', 'ʷen', 'tʰw', 'ʷɤ̆', 'ʷiu', 'kwi', 'ŋ͡m', 'k͡p', 'cw', 'jw', 'uə', 'eə', 'bw', 'oj', 'ʷi', 'vw', 'ăw', 'ʈw', 'ʂw', 'aʊ', 'fw', 'ɛu', 'tʰ', 'tʃ', 'ɔɪ', 'xw', 'ʷɤ', 'ɤ̆', 'ŋw', 'ʊə', 'zi', 'ʷă', 'dw', 'eɪ', 'aɪ', 'ew', 'iə', 'ɣw', 'zw', 'ɯj', 'ʷɛ', 'ɯw', 'ɤj', 'ɔ:', 'əʊ', 'ʷa', 'mw', 'ɑ:', 'hw', 'ɔj', 'uj', 'lw', 'ɪə', 'ăj', 'u:', 'aw', 'ɛj', 'iw', 'aj', 'ɜ:', 'kw', 'nw', 't∫', 'ɲw', 'eo', 'sw', 'tw', 'ʐw', 'iɛ', 'ʷe', 'i:', 'ɯə', 'dʒ', 'ɲ', 'θ', 'ʌ', 'l', 'w', '1', 'ɪ', 'ɯ', 'd', '∫', 'p', 'ə', 'u', 'o', '3', 'ɣ', '!', 'ð', 'ʧ', '6', 'ʒ', 'ʐ', 'z', 'v', 'g', 'ă', '_', 'æ', 'ɤ', '2', 'ʤ', 'i', '.', 'ɒ', 'b', 'h', 'n', 'ʂ', 'ɔ', 'ɛ', 'k', 'm', '5', ' ', 'c', 'j', 'x', 'ʈ', ',', '4', 'ʊ', 's', 'ŋ', 'a', 'ʃ', '?', 'r', ':', 'η', 'f', ';', 'e', 't', "'"]

_PAD_ = 'PAD'

symbols = [_PAD_] + vietnamese_phoneme

symbol_to_id = {v:k for k, v in enumerate(symbols)}

def viphoneme_to_index(text):
    text = text.split('/')[1:-1]

    text = [symbol_to_id[i] for i in text]
    return text


