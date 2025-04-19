import torch
from fhe_ai_inference.core import FHEInference
from torch import nn

model = nn.Sequential(
    nn.Linear(4, 2),
)

fhe = FHEInference(model)

x = torch.tensor([1.0, 2.0, 3.0, 4.0])

output = fhe.predict(x)
print("Decrypted output:", output)
