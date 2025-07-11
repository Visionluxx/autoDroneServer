import torch  
torch.cuda.empty_cache()  
!git clone https://github.com/apple/ml-depth-pro.git  
%cd ml-depth-pro  
!pip install -e .   
!pip install timm einops  
!bash get_pretrained_models.sh  
