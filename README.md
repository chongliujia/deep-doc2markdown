# Deep Doc2Markdown

<div align="right">
  <a href="#中文文档">中文文档</a> | <a href="#english-documentation">English</a>
</div>

## English Documentation

A powerful document-to-markdown converter that extracts text and images from PDF, Word documents, and images, using OCR where needed, to generate clean Markdown output.

### Features

- **Document Processing**:
  - Extract text and images from PDF and Word documents
  - Process standalone images with OCR
  - Use PaddleOCR for high-quality optical character recognition
  - Convert document structure to proper Markdown formatting
  - Smart handling of multi-column layouts

- **Modern User Interface**:
  - Clean, responsive design with Bootstrap 5
  - Drag & drop file upload interface
  - Real-time conversion status display
  - Tabbed interface for viewing Markdown, original document, and rendered preview
  - Syntax highlighting for Markdown code
  - Content scrolling with custom scrollbars for long documents
  - Smart paragraph detection and formatting for better readability
  - Optimized layout for both desktop and mobile devices
  - Dark mode support

- **User Experience**:
  - Copy Markdown to clipboard with one click
  - Download converted Markdown as a file
  - Print functionality for rendered Markdown
  - Instant rendering of Markdown to HTML preview
  - Error handling with descriptive messages
  - Auto-refresh UI components

### Technologies

- **Frontend**:
  - HTML5, CSS3, and JavaScript (ES6+)
  - Bootstrap 5 for responsive design
  - Highlight.js for syntax highlighting
  - Marked.js for Markdown rendering
  - Custom CSS for enhanced UI components
  - AnimateCSS for smooth transitions

- **Backend**:
  - Python 3.8+ with FastAPI
  - PyPDF2 for PDF processing
  - python-docx for Word document processing
  - PaddleOCR for image text recognition
  - Jinja2 for templating
  - Asynchronous processing for improved performance

- **Data Processing**:
  - Text cleaning and formatting algorithms
  - Smart paragraph detection
  - Intelligent handling of document structure
  - Image extraction and processing
  - OCR confidence scoring and validation

### Project Structure

```
document-to-markdown/
│
├── app/
│   ├── core/
│   │   ├── document_extractor/      # Extract content from documents
│   │   │   ├── pdf_extractor.py     # Extract text and images from PDF
│   │   │   ├── docx_extractor.py    # Extract text and images from Word
│   │   │   └── image_handler.py     # Process standalone images
│   │   │
│   │   ├── ocr/
│   │   │   ├── paddle_ocr.py        # PaddleOCR implementation
│   │   │   └── ocr_processor.py     # OCR processing workflow
│   │   │
│   │   ├── text_processor/          # Text processing module
│   │   │   ├── text_cleaner.py      # Text cleaning
│   │   │   └── text_merger.py       # Merge document and OCR text
│   │   │
│   │   └── markdown_converter/      # Markdown conversion module
│   │       ├── md_formatter.py      # Text to Markdown conversion
│   │       ├── image_formatter.py   # Image processing and Markdown syntax
│   │       └── structure_parser.py  # Parse document structure
│   │
│   ├── media/                       # Store processed images
│   │   └── images/                  
│   │
│   ├── api/                         # API endpoints
│   │   ├── document_api.py          # Document processing API
│   │   └── static_files.py          # Serve static files
│   │
│   ├── models/                      # Data models
│   │   └── document_models.py       # Document data models
│   │
│   └── frontend/                    # Web interface
│       ├── frontend_api.py          # Frontend API
│       └── templates/               # HTML templates
│           └── index.html           # Main app page
│
├── config/                          # Configuration
│   └── config.py                    # App configuration
│
├── requirements.txt                 # Dependencies
└── main.py                          # Main application
```

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/deep-doc2markdown.git
   cd deep-doc2markdown
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install PaddlePaddle:
   
   Depending on your system, you might need specific installation instructions for PaddlePaddle. Visit the [PaddlePaddle installation guide](https://www.paddlepaddle.org.cn/en/install/quick) for details.

### Usage

1. Start the application:
   ```
   python main.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

3. Use the web interface to upload your documents and convert them to Markdown.

### API Endpoints

- `POST /api/upload`: Upload a document for conversion
- `GET /api/status/{doc_id}`: Check the status of a conversion job
- `GET /api/markdown/{doc_id}`: Get the generated Markdown content

### Development

#### Requirements

- Python 3.8+
- FastAPI
- PyPDF2 for PDF processing
- python-docx for Word document processing
- PaddleOCR for image text recognition
- Jinja2 for templating

#### Configuration

Edit `config/config.py` to adjust settings:

- Change the server host and port
- Configure OCR settings
- Modify file storage paths

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgements

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) for the OCR functionality
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [PyPDF2](https://pythonhosted.org/PyPDF2/) for PDF processing
- [Bootstrap](https://getbootstrap.com/) for the UI framework
- [Highlight.js](https://highlightjs.org/) for code highlighting
- [Marked.js](https://marked.js.org/) for Markdown parsing

---

<h1 id="中文文档">Deep Doc2Markdown</h1>

<div align="right">
  <a href="#中文文档">中文文档</a> | <a href="#english-documentation">English</a>
</div>

一个强大的文档转Markdown转换工具，能够从PDF、Word文档和图像中提取文本和图像，在需要时使用OCR，生成整洁的Markdown输出。

### 功能特性

- **文档处理**：
  - 从PDF和Word文档中提取文本和图像
  - 使用OCR处理独立图像
  - 使用PaddleOCR进行高质量的光学字符识别
  - 将文档结构转换为适当的Markdown格式
  - 智能处理多列布局

- **现代用户界面**：
  - 使用Bootstrap 5的清晰、响应式设计
  - 拖放式文件上传界面
  - 实时转换状态显示
  - 用于查看Markdown、原始文档和渲染预览的标签式界面
  - Markdown代码语法高亮
  - 长文档的内容滚动和自定义滚动条
  - 智能段落检测和格式化，提高可读性
  - 针对桌面和移动设备优化的布局
  - 深色模式支持

- **用户体验**：
  - 一键复制Markdown到剪贴板
  - 将转换后的Markdown下载为文件
  - 渲染后的Markdown打印功能
  - Markdown即时渲染为HTML预览
  - 带有描述性消息的错误处理
  - 自动刷新UI组件

### 技术栈

- **前端**：
  - HTML5、CSS3和JavaScript（ES6+）
  - Bootstrap 5用于响应式设计
  - Highlight.js用于语法高亮
  - Marked.js用于Markdown渲染
  - 增强UI组件的自定义CSS
  - AnimateCSS用于平滑过渡效果

- **后端**：
  - Python 3.8+配合FastAPI
  - PyPDF2用于PDF处理
  - python-docx用于Word文档处理
  - PaddleOCR用于图像文本识别
  - Jinja2用于模板渲染
  - 异步处理提高性能

- **数据处理**：
  - 文本清理和格式化算法
  - 智能段落检测
  - 智能处理文档结构
  - 图像提取和处理
  - OCR置信度评分和验证

### 项目结构

```
document-to-markdown/
│
├── app/
│   ├── core/
│   │   ├── document_extractor/      # 从文档中提取内容
│   │   │   ├── pdf_extractor.py     # 从PDF中提取文本和图像
│   │   │   ├── docx_extractor.py    # 从Word中提取文本和图像
│   │   │   └── image_handler.py     # 处理独立图像
│   │   │
│   │   ├── ocr/
│   │   │   ├── paddle_ocr.py        # PaddleOCR实现
│   │   │   └── ocr_processor.py     # OCR处理工作流
│   │   │
│   │   ├── text_processor/          # 文本处理模块
│   │   │   ├── text_cleaner.py      # 文本清理
│   │   │   └── text_merger.py       # 合并文档和OCR文本
│   │   │
│   │   └── markdown_converter/      # Markdown转换模块
│   │       ├── md_formatter.py      # 文本到Markdown转换
│   │       ├── image_formatter.py   # 图像处理和Markdown语法
│   │       └── structure_parser.py  # 解析文档结构
│   │
│   ├── media/                       # 存储处理过的图像
│   │   └── images/                  
│   │
│   ├── api/                         # API端点
│   │   ├── document_api.py          # 文档处理API
│   │   └── static_files.py          # 提供静态文件
│   │
│   ├── models/                      # 数据模型
│   │   └── document_models.py       # 文档数据模型
│   │
│   └── frontend/                    # Web界面
│       ├── frontend_api.py          # 前端API
│       └── templates/               # HTML模板
│           └── index.html           # 主应用页面
│
├── config/                          # 配置
│   └── config.py                    # 应用配置
│
├── requirements.txt                 # 依赖项
└── main.py                          # 主应用程序
```

### 安装

1. 克隆仓库：
   ```
   git clone https://github.com/yourusername/deep-doc2markdown.git
   cd deep-doc2markdown
   ```

2. 创建虚拟环境（可选但推荐）：
   ```
   python -m venv venv
   source venv/bin/activate  # 在Windows上：venv\Scripts\activate
   ```

3. 安装依赖项：
   ```
   pip install -r requirements.txt
   ```

4. 安装PaddlePaddle：
   
   根据您的系统，您可能需要特定的PaddlePaddle安装说明。访问[PaddlePaddle安装指南](https://www.paddlepaddle.org.cn/install/quick)了解详情。

### 使用方法

1. 启动应用程序：
   ```
   python main.py
   ```

2. 打开浏览器并导航至：
   ```
   http://127.0.0.1:8000
   ```

3. 使用Web界面上传您的文档并将其转换为Markdown。

### API端点

- `POST /api/upload`：上传文档进行转换
- `GET /api/status/{doc_id}`：检查转换作业的状态
- `GET /api/markdown/{doc_id}`：获取生成的Markdown内容

### 开发

#### 要求

- Python 3.8+
- FastAPI
- PyPDF2用于PDF处理
- python-docx用于Word文档处理
- PaddleOCR用于图像文本识别
- Jinja2用于模板渲染

#### 配置

编辑`config/config.py`调整设置：

- 更改服务器主机和端口
- 配置OCR设置
- 修改文件存储路径

### 许可证

该项目采用MIT许可证 - 有关详细信息，请参阅LICENSE文件。

### 致谢

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)提供OCR功能
- [FastAPI](https://fastapi.tiangolo.com/)提供Web框架
- [PyPDF2](https://pythonhosted.org/PyPDF2/)用于PDF处理
- [Bootstrap](https://getbootstrap.com/)提供UI框架
- [Highlight.js](https://highlightjs.org/)用于代码高亮
- [Marked.js](https://marked.js.org/)用于Markdown解析
