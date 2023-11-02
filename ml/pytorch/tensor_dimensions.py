import torch

t1 = torch.arange(start=1, end=13, step=1)
print(t1, t1.shape)

print(t1.reshape(3,4))

print(torch.stack([t1, t1, t1], dim=1))
