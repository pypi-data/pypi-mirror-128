def get_linear_lambda_with_warmup(num_warmup_steps, num_training_steps):
    
    def lr_lambda(current_step: int):
        if current_step < num_warmup_steps:
            return 1.0
        return max(
            0.0, float(num_training_steps - current_step) / float(max(1, num_training_steps - num_warmup_steps))
        )

    return lr_lambda
