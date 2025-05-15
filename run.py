import uvicorn
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

# 创建FastAPI应用
app = FastAPI(
    title="文档转Markdown工具",
    description="将PDF、Word文档和图片转换为Markdown",
    version="1.0.0"
)

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取当前目录
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "app" / "frontend" / "templates"
MEDIA_DIR = BASE_DIR / "app" / "media"
IMAGES_DIR = MEDIA_DIR / "images"

# 确保目录存在
os.makedirs(IMAGES_DIR, exist_ok=True)

# 挂载静态文件
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

# 首页路由
@app.get("/")
async def get_index():
    """
    提供主页面。
    """
    return FileResponse(TEMPLATES_DIR / "index.html")

# 启动服务器
if __name__ == "__main__":
    uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=True) 