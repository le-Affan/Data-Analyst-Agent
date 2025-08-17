# Data Analyst Agent

A multi-modal AI-powered data analyst agent that can process and analyze various file types including CSV, Excel, text files, PDFs, and images. Built with Python and Streamlit, this tool leverages Together AI's LLaMA model to provide intelligent insights about your data.

## ✨ Features

- **Multi-format File Support**: Upload and analyze CSV, Excel, TXT, PDF, PNG, JPG, and JPEG files
- **AI-Powered Analysis**: Uses LLaMA-4-Maverick model through Together AI for intelligent data interpretation
- **Interactive Web Interface**: Clean, user-friendly Streamlit interface
- **Voice Input**: Optional speech-to-text functionality for asking questions
- **Automatic EDA**: Built-in exploratory data analysis with visualizations
- **OCR Support**: Extract text from images using Tesseract OCR
- **Conversation Logging**: All interactions are logged for reference

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR (for image text extraction)
- Together AI API key

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/le-Affan/Data-Analyst-Agent.git
   cd Data-Analyst-Agent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**:
   - **Windows**: Download from [GitHub Tesseract releases](https://github.com/tesseract-ocr/tesseract/releases)
   - **macOS**: `brew install tesseract`
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Together AI API key
   ```

## 🚀 Usage

### Web Application (Streamlit)

1. **Start the Streamlit app**:
   ```bash
   streamlit run src/streamlit_app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Upload a file** using the file uploader

4. **Ask questions** about your data in the text input field

5. **Optional**: Use voice input by clicking the "Record Audio" button

### Jupyter Notebook

Alternatively, you can use the Jupyter notebook for interactive analysis:

```bash
jupyter notebook notebooks/data_analysis_notebook.ipynb
```

## 📁 Project Structure

```
Data-Analyst-Agent/
├── src/                          # Source code
│   ├── streamlit_app.py         # Main Streamlit application
│   ├── data_processor.py        # Data processing utilities
│   ├── ai_agent.py              # AI agent functionality
│   └── utils.py                 # Helper functions
├── notebooks/                   # Jupyter notebooks
│   └── data_analysis_notebook.ipynb
├── data/                        # Sample data files
│   ├── samples/                 # Sample datasets
│   └── outputs/                 # Generated outputs
├── config/                      # Configuration files
│   └── config.yaml             # Application configuration
├── logs/                        # Log files
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
TOGETHER_API_KEY=your_together_ai_api_key_here
TESSERACT_PATH=path_to_tesseract_executable  # Optional, for custom Tesseract path
LOG_LEVEL=INFO
```

### Supported File Types

- **CSV Files**: Pandas-based analysis
- **Excel Files**: Support for .xlsx and .xls formats
- **Text Files**: Plain text processing
- **PDF Files**: Text extraction using pdfplumber
- **Images**: OCR text extraction (PNG, JPG, JPEG)

## 🤖 AI Model

This project uses the **LLaMA-4-Maverick-17B-128E-Instruct-FP8** model through Together AI's API. This model provides:

- Advanced natural language understanding
- Context-aware responses
- Data interpretation capabilities
- Support for multiple languages

## 📊 Sample Data

The `data/samples/` directory contains sample datasets for testing:

- `personality_dataset.csv` - Sample personality analysis data
- `sales_report.xlsx` - Sample sales data for Excel testing

## 📝 Logging

All interactions are automatically logged:

- **Agent responses**: `logs/agent_responses.txt`
- **User interactions**: `logs/interaction_log.txt`
- **Application logs**: `logs/app.log`

## 🔍 Features in Detail

### Exploratory Data Analysis (EDA)

- Automatic statistical summaries
- Distribution plots for numerical columns
- Correlation heatmaps
- Missing data analysis

### Voice Input

- Real-time speech recognition
- Google Speech Recognition API
- Hands-free question asking

### Multi-modal Processing

- Intelligent file type detection
- Appropriate processing pipeline for each file type
- Unified query interface across all file types

## 🚨 Security Notes

- Never commit your API keys to version control
- Use environment variables for sensitive configuration
- The `.env` file is excluded from git by default

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/le-Affan/Data-Analyst-Agent/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🔮 Future Enhancements

- [ ] Support for more file formats (JSON, XML, etc.)
- [ ] Advanced visualization options
- [ ] Database connectivity
- [ ] Batch processing capabilities
- [ ] Custom model fine-tuning
- [ ] Web scraping integration
- [ ] Real-time data streaming

---

**Built with ❤️ by [Affan Shaikh](https://github.com/le-Affan)**
