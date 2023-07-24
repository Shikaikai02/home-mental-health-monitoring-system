import torch
import cv2

print(torch.__version__)

tensor1 = torch.tensor([1,2,3])
tensor1.cuda()