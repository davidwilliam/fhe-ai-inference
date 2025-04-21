# scripts/test_openfhe_init.py

from fhe_ai_inference.fheai import FHEAI


def main():
    try:
        FHEAI(mult_depth=2, scale_mod_size=50)
        print("✅ OpenFHE context successfully initialized with CKKS.")
    except Exception as e:
        print("❌ Failed to initialize FHE context.")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
