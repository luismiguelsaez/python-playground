import torch

print("Using PyTorch version: {}".format(torch.__version__))

# Scalar

scalar = torch.tensor(3.1415)
print("Scalar dimensions: {}".format(scalar.ndim))
print("Scalar shape: {}".format(scalar.shape))

# Vector

vector = torch.tensor([1, 2, 3, 4, 5])
print("Vector dimensions: {}".format(vector.ndim))
print("Vector shape: {}".format(vector.shape))

# Matrix

MATRIX = torch.tensor([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9]])
print("Matrix dimensions: {}".format(MATRIX.ndim))
print("Matrix shape: {}".format(MATRIX.shape))

# Tensor

TENSOR = torch.tensor([[[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9]]])
print("Tensor dimensions: {}".format(TENSOR.ndim))
print("Tensor shape: {}".format(TENSOR.shape))
