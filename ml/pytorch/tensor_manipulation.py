import torch

tensor_1 = torch.rand(size=(3, 4))
tensor_2 = torch.rand(size=(3, 4))

# Addition

print(torch.add(tensor_1, tensor_2))

# Subtraction

print(torch.sub(tensor_1, 10))

# Multiplication
print(torch.mul(tensor_1, 10))

# Division

print(torch.div(tensor_1, 10))


