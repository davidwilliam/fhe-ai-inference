import torch
from torch import nn

from fhe_ai_inference.core import FHEInference


def test_secure_inference_runs():
    # Define simple test model: Linear(4 → 2)
    model = nn.Sequential(nn.Linear(4, 2))
    fhe = FHEInference(model)

    # Input vector
    input_tensor = torch.tensor([1.0, 2.0, 3.0, 4.0])

    # Run secure inference
    output = fhe.predict(input_tensor)

    # Should return a 2-element vector (after square activation)
    assert isinstance(output, torch.Tensor)
    assert output.shape == torch.Size([2])
