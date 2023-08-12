import re
import torch

# Create float32 tensor

float_32_tensor = torch.tensor([1.2, 2, 3.],
                              dtype=torch.float32,
                              device="cpu", # CPU or GPU
                              requires_grad=False) # Whether to track operations on this tensor to calculate gradients later
print("Float32 tensor: {} {}".format(float_32_tensor.shape, float_32_tensor.dtype))
print("Float32 tensor:\n{}".format(float_32_tensor))

# Create float16 tensor

float_16_tensor = torch.tensor([1.2, 2, 3.],
                               dtype=torch.float16,
                               device="cpu",
                               requires_grad=False)
print("Float16 tensor: {} {}".format(float_16_tensor.shape, float_16_tensor.dtype))
print("Float16 tensor:\n{}".format(float_16_tensor))

print(float_16_tensor * float_32_tensor)

