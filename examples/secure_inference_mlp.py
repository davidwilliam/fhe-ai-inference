import torch
from torch import nn

from fhe_ai_inference.core import FHEInference

model = nn.Sequential(
    nn.Linear(4, 2),
)

fhe = FHEInference(model)

x = torch.tensor([1.0, 2.0, 3.0, 4.0])

output = fhe.predict(x)
print("Decrypted output:", output)
