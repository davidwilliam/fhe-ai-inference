def square_activation(ciphertext, evaluator):
    result = evaluator.square(ciphertext)
    evaluator.relinearize_inplace(result)
    return result
