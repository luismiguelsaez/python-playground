import torch

print("Using PyTorch version: {}".format(torch.__version__))

# Tensor

TENSOR = torch.tensor([[[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9]]])
print("Tensor dimensions: {}".format(TENSOR.ndim))
print("Tensor shape: {}".format(TENSOR.shape))

# Random tensors

random_tensor = torch.rand(3, 4)
print("Random tensor:")
print(random_tensor)

# Create a random tensor with similar shape as an image tensor

random_image_size_tensor = torch.rand(size=(224, 224, 3)) # 224x224 RGB image
print("Random image size tensor: {} {}".format(random_image_size_tensor.shape, random_image_size_tensor.ndim))

# Zeros and ones tensors

zeros_tensor = torch.zeros(size=(3, 4))
print("Zeros tensor: {} {}".format(zeros_tensor.shape, zeros_tensor.ndim))
print(zeros_tensor)

# Ones tensor

ones_tensor = torch.ones(size=(3, 4))
print("Ones tensor: {} {}".format(ones_tensor.shape, ones_tensor.ndim))
print(ones_tensor)

# Create a range of tensors

range_tensor = torch.arange(start=0, end=11, step=1)
print("Range tensor:\n",range_tensor)

# Create a tensor like another tensor

like_tensor = torch.zeros_like(input=range_tensor)
print("Like tensor:\n",like_tensor)
