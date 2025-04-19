import torch
from fhe_ai_inference.core import FHEInference
from torch import nn

# Toy model: 2-layer MLP with 4 input neurons, 2 output
model = nn.Sequential(
    nn.Linear(4, 2),
)

# Initialize secure inference engine
fhe = FHEInference(model)

# Sample input
x = torch.tensor([1.0, 2.0, 3.0, 4.0])

# Perform secure inference
output = fhe.predict(x)
print("Decrypted output:", output)
