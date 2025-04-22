import numpy as np

from fhe_ai_inference.fheai import FHEAI


def main():
    # Initialize bootstrappable context with safe margins
    fhe = FHEAI(
        bootstrappable=True,
        level_budget=[6, 6],
        scale_mod_size=59,
        num_slots=128,
        ring_dim=1 << 15,
    )

    # Encryption level before multiplications
    values = [0.25, 0.5, 0.75, 1.0, 2.0, 3.0, 4.0, 5.0]
    depth = sum(fhe.level_budget) + 7
    initial_level = depth - 4

    print(f"🔒 Encrypting at level {initial_level}: {values}")
    ciph = fhe.encrypt(values, level=initial_level)

    print(f"➡️  Ciphertext level before multiplications: {ciph.GetLevel()}")
    for i in range(4):
        ciph = fhe.multiply_and_rescale(ciph, ciph)
        print(f"🔁 After multiplication {i+1}: level = {ciph.GetLevel()}")

    print(f"➡️  Ciphertext level before bootstrap: {ciph.GetLevel()}")

    # This will now *automatically bootstrap* inside decrypt if needed
    ciph = fhe.mod_reduce(ciph)  # Pre-align for safety
    if fhe._bootstrappable:
        ciph = fhe.bootstrap(ciph)
        print(f"✅ Ciphertext level after bootstrap: {ciph.GetLevel()}")

    result = fhe.decrypt(ciph, length=len(values))
    print(f"🔓 Decrypted result after bootstrap: {result}")

    expected = np.power(values, 16)
    close_mask = np.isclose(result, expected, rtol=1e-2, atol=1e-3)
    print(f"✅ Acceptable tolerance? {np.all(close_mask)}")


if __name__ == "__main__":
    main()
