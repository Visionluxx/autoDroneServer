%cd /content/ml-depth-pro  
from depth_pro import create_model_and_transforms, load_rgb  
import torch  
from PIL import Image  
  
model, transform = create_model_and_transforms()  
model.eval().cuda()  # hoặc .cpu() nếu không dùng GPU  
