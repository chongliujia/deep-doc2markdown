# deep-doc2markdown


```
document-to-markdown/
│
├── app/
│   ├── core/
│   │   ├── document_extractor/      # 从文档中提取内容
│   │   │   ├── pdf_extractor.py     # 从PDF提取文本和图片
│   │   │   ├── docx_extractor.py    # 从Word提取文本和图片
│   │   │   └── image_handler.py     # 处理单独上传的图片
│   │   │
│   │   ├── ocr/
│   │   │   ├── paddle_ocr.py        # PaddleOCR实现
│   │   │   └── ocr_processor.py     # OCR处理流程
│   │   │
│   │   ├── text_processor/          # 文本处理模块
│   │   │   ├── text_cleaner.py      # 文本清洗
│   │   │   └── text_merger.py       # 合并文档和OCR文本
│   │   │
│   │   └── markdown_converter/      # Markdown转换模块
│   │       ├── md_formatter.py      # 文本转Markdown
│   │       ├── image_formatter.py   # 图片处理和生成Markdown图片语法
│   │       └── structure_parser.py  # 解析文档结构(标题、列表等)
│   │
│   ├── media/                       # 存储处理过的图片
│   │   └── images/                  
│   │
│   ├── api/                         # API接口
│   └── models/                      # 数据模型
│
├── config/                          # 配置文件
├── requirements.txt
└── main.py
```

## 处理流程

### 文档上传与解析:

1. 接收用户上传的文档(PDF、Word)或图片
2. 提取文档中的文本内容，保留格式信息
3. 从文档中提取图片并保存

### 图片处理:

1. 将提取的图片保存到media/images目录
2. 为每个图片生成唯一ID和访问URL
3. 使用PaddleOCR进行图片内容识别
4. 生成图片描述（基于OCR结果）

### Markdown转换:

1. 将文本内容转换为Markdown格式
2. 识别标题、列表、表格等结构并转换为对应Markdown语法
3. 对于图片，生成![图片描述](图片URL)格式
4. 保持文档的原始结构和层次

### 结果输出:

1. 提供完整的Markdown文档
2. 图片链接可以是相对路径或完整URL
3. 提供下载选项或API接口
