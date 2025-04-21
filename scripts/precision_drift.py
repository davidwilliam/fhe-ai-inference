# scripts/precision_drift.py

from fhe_ai_inference.fheai import FHEAI


def run_precision_drift_test(value=3.14159, depth=4, scale=50, iterations=10):
    fhe = FHEAI(mult_depth=depth, scale_mod_size=scale)
    encrypted = fhe.encrypt(value)

    print(f"Initial Value: {value}")
    print("\nDrift over repeated multiplications:\n")
    print(f"{'Step':<5} | {'Decrypted Value':<20} | {'Absolute Error':<20}")
    print("-" * 55)

    current = encrypted
    for i in range(1, iterations + 1):
        try:
            current = fhe.multiply(current, encrypted)
            decrypted = fhe.decrypt(current, length=1)[0]
            error = abs(decrypted - (value ** (i + 1)))
            print(f"{i:<5} | {decrypted:<20.10f} | {error:<20.10f}")
        except Exception as e:
            print(f"{i:<5} | {'DECRYPTION FAILED':<20} | {'---'}")
            print(f"\n[Expected result]: ❌ Decryption failed at step {i}: {e}")
            break


if __name__ == "__main__":
    run_precision_drift_test()
