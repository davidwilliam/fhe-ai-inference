# scripts/test_openfhe_init.py
from fhe_ai_inference.openfhe_ckks import CKKSOperations

ckks = CKKSOperations(slots=2)
print("Context successfully created.")
