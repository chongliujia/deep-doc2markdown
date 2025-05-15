from paddleocr import PaddleOCR
import os

def test_paddleocr():
    # 初始化PaddleOCR
    print("初始化PaddleOCR...")
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    
    # 设置测试图像路径（可以是任何包含文字的图像）
    # 如果没有测试图像，可以使用以下代码创建一个简单的测试图像
    from PIL import Image, ImageDraw, ImageFont
    
    # 创建测试图像
    print("创建测试图像...")
    img = Image.new('RGB', (300, 100), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("Arial.ttf", 15)
    except:
        # 如果找不到特定字体，使用默认字体
        font = ImageFont.load_default()
    
    d.text((10, 10), "这是一个测试文本 Hello World", font=font, fill=(0,0,0))
    
    # 保存测试图像
    test_img_path = "test_ocr_image.png"
    img.save(test_img_path)
    
    # 执行OCR识别
    print("执行OCR识别...")
    try:
        result = ocr.ocr(test_img_path, cls=True)
        
        # 打印结果
        print("OCR识别结果:")
        for line in result:
            for item in line:
                print(f"文本: {item[1][0]}, 置信度: {item[1][1]}")
        
        print("PaddleOCR 2.10.0 工作正常！")
        
        # 删除测试图像
        os.remove(test_img_path)
        return True
    except Exception as e:
        print(f"OCR识别出错: {e}")
        return False

if __name__ == "__main__":
    test_paddleocr() 