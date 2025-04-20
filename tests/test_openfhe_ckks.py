from fhe_ai_inference.openfhe_ckks import CKKSOperations


def test_ckks_operations_add_mult_list():
    # Initialize CKKSOperations
    ckks = CKKSOperations(slots=2, poly_modulus_degree=16384, scaling_modulus_size=45)

    # Encrypt an input
    input_values = [1.0, 2.0]
    ciphertext = ckks.encrypt(input_values)

    # Test eval_add with a list (hits the isinstance branch)
    add_result = ckks.eval_add(ciphertext, [1.0, 1.0])
    decrypted_add = ckks.decrypt(add_result)
    expected_add = [2.0, 3.0]  # [1.0+1.0, 2.0+1.0]
    for actual, exp in zip(decrypted_add, expected_add):
        assert abs(actual - exp) <= 0.1, f"Add expected {exp}, got {actual}"

    # Test eval_mult with a list (hits the isinstance branch)
    mult_result = ckks.eval_mult(ciphertext, [2.0, 2.0])
    decrypted_mult = ckks.decrypt(mult_result)
    expected_mult = [2.0, 4.0]  # [1.0*2.0, 2.0*2.0]
    for actual, exp in zip(decrypted_mult, expected_mult):
        assert abs(actual - exp) <= 0.1, f"Mult expected {exp}, got {actual}"


def test_ckks_operations_sum():
    # Initialize CKKSOperations
    ckks = CKKSOperations(slots=3, poly_modulus_degree=16384, scaling_modulus_size=45)

    # Encrypt an input
    input_values = [1.0, 2.0, 3.0]
    ciphertext = ckks.encrypt(input_values)

    # Test eval_sum
    sum_result = ckks.eval_sum(ciphertext)
    decrypted_sum = ckks.decrypt(sum_result)
    print(f"Decrypted sum: {decrypted_sum}")  # Debug output
    expected_sum = 6.0  # Sum of [1.0, 2.0, 3.0] = 6.0 in first slot
    assert (
        abs(decrypted_sum[0] - expected_sum) <= 0.1
    ), f"Sum expected {expected_sum}, got {decrypted_sum[0]}"


def test_ckks_operations_decrypt_no_trim():
    # Initialize CKKSOperations
    ckks = CKKSOperations(slots=2, poly_modulus_degree=16384, scaling_modulus_size=45)

    # Encrypt an input
    input_values = [1.0, 2.0]
    ciphertext = ckks.encrypt(input_values)

    # Decrypt without trimming
    decrypted = ckks.decrypt(ciphertext, trim=False)
    assert len(decrypted) >= ckks.active_slots, "Expected at least active_slots values"
    expected = [1.0, 2.0]
    for actual, exp in zip(decrypted[:2], expected):
        assert abs(actual - exp) <= 0.1, f"Expected {exp}, got {actual}"


def test_ckks_operations_single_slot():
    # Initialize CKKSOperations with slots=1
    ckks = CKKSOperations(slots=1, poly_modulus_degree=16384, scaling_modulus_size=45)

    # Encrypt a single value
    input_values = [2.0]
    ciphertext = ckks.encrypt(input_values)

    # Decrypt to verify
    decrypted = ckks.decrypt(ciphertext)
    assert abs(decrypted[0] - 2.0) <= 0.1, f"Expected 2.0, got {decrypted[0]}"


def test_ckks_operations_add_mult_ciphertext():
    # Initialize CKKSOperations
    ckks = CKKSOperations(slots=2, poly_modulus_degree=16384, scaling_modulus_size=45)

    # Encrypt two inputs
    input1 = [1.0, 2.0]
    input2 = [2.0, 3.0]
    ciphertext1 = ckks.encrypt(input1)
    ciphertext2 = ckks.encrypt(input2)

    # Test eval_add with ciphertext
    add_result = ckks.eval_add(ciphertext1, ciphertext2)
    decrypted_add = ckks.decrypt(add_result)
    expected_add = [3.0, 5.0]  # [1.0+2.0, 2.0+3.0]
    for actual, exp in zip(decrypted_add, expected_add):
        assert abs(actual - exp) <= 0.1, f"Add expected {exp}, got {actual}"

    # Test eval_mult with ciphertext
    mult_result = ckks.eval_mult(ciphertext1, ciphertext2)
    decrypted_mult = ckks.decrypt(mult_result)
    expected_mult = [2.0, 6.0]  # [1.0*2.0, 2.0*3.0]
    for actual, exp in zip(decrypted_mult, expected_mult):
        assert abs(actual - exp) <= 0.1, f"Add expected {exp}, got {actual}"
