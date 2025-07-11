from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
import io


app = FastAPI()
templates=Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
  return HTMLResponse("hello")

@app.post("/upload")
async def get_data(request: Request, image: UploadFile=File(...)):
    droneImage=await image.read()
    import numpy as np
    import cv2
    nparr = np.frombuffer(droneImage, np.uint8)
    fileImage = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite("/content/a.jpg", fileImage)
    from depth_pro import create_model_and_transforms, load_rgb
    import torch
    from PIL import Image

    img, _, f_px = load_rgb("/content/a.jpg")
    inp = transform(img).unsqueeze(0).cuda()

    with torch.no_grad():
        prediction = model.infer(inp, f_px=f_px)

    depth_map = prediction["depth"]  # float32 (mét)
    to_cpu=depth_map.cpu().detach().numpy()
    front_map = np.array(to_cpu)

    import numpy as np
    import matplotlib.pyplot as plt

    plt.subplot(1, 2, 2)
    plt.title("Depth map (mét)")
    plt.imshow(front_map, cmap='plasma')
    plt.colorbar(label="mét")
    plt.axis("off")
    plt.show()

    import gc
    import torch

    # Xóa biến nếu không còn dùng nữa
    del prediction, depth_map
    gc.collect()

    # Giải phóng bộ nhớ GPU
    torch.cuda.empty_cache()

import nest_asyncio
import uvicorn

# Cho phép chạy uvicorn nhiều lần trong Colab
nest_asyncio.apply()

import subprocess
import re

def start_cloudflared():
    cmd = ["./cloudflared", "tunnel", "--url", "http://localhost:8000", "--no-autoupdate"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    url = None
    for line in proc.stdout:
        print(line.strip())  # log ra để kiểm tra
        match = re.search(r"https://.*\.trycloudflare.com", line)
        if match:
            url = match.group(0)
            break
    return url

public_url = start_cloudflared()
print("🌐 Truy cập tại:", public_url)

# Chạy app
uvicorn.run(app, host="localhost", port=8000)
