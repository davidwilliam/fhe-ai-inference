def square_activation(ciphertext, evaluator):
    result = evaluator.EvalMult(ciphertext, ciphertext)
    evaluator.Relinearize(result)
    return result
