# getting_started_with_openfhe.py
import numpy as np

from fhe_ai_inference.fheai import FHEAI

# Initialize FHE context
fheai = FHEAI(mult_depth=2, scale_mod_size=50)

# Encrypt and decrypt example
data = np.array([1.5, 2.5, 3.5])

# Encrypt the data
encrypted_data = fheai.encrypt(data)

# Decrypt the data (specify length to match original data size)
decrypted_data = fheai.decrypt(encrypted_data, length=len(data))

print("Encryption/Decryption Example")
print("Original:", data)
print("Decrypted:", decrypted_data)
print("\n")

# Homomorphic addition example
data1 = np.array([1, 2, 3])
data2 = np.array([4, 5, 6])

enc1 = fheai.encrypt(data1)
enc2 = fheai.encrypt(data2)

enc_sum = fheai.add(enc1, enc2)
dec_sum = fheai.decrypt(enc_sum, length=len(data1))

print("Homomorphic Addition Example")
print("Data1:", data1)
print("Data2:", data2)
print("Sum:", dec_sum)
print("\n")

# Homomorphic multiplication example
data3 = np.array([2, 3, 4])
data4 = np.array([5, 6, 7])

enc3 = fheai.encrypt(data3)
enc4 = fheai.encrypt(data4)

enc_product = fheai.multiply(enc3, enc4)
dec_product = fheai.decrypt(enc_product, length=len(data3))

print("Homomorphic Multiplication Example")
print("Data3:", data3)
print("Data4:", data4)
print("Product:", dec_product)
