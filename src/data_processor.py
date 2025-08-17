"""
Data Processor Module
Handles processing of various file types including CSV, Excel, PDF, images, and text files
"""

import pandas as pd
import pdfplumber
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging
from io import StringIO
from typing import Union, Dict, Any
import tempfile

class DataProcessor:
    """Class for processing different types of data files"""
    
    def __init__(self):
        """Initialize the DataProcessor"""
        self.logger = logging.getLogger(__name__)
        self.setup_tesseract()
    
    def setup_tesseract(self):
        """Setup Tesseract OCR path if specified in environment"""
        tesseract_path = os.getenv("TESSERACT_PATH")
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            self.logger.info(f"Tesseract path set to: {tesseract_path}")
    
    def process_file(self, uploaded_file) -> Union[pd.DataFrame, str, None]:
        """
        Process uploaded file based on its type
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Processed data (DataFrame for structured data, str for text)
        """
        if uploaded_file is None:
            return None
        
        file_extension = uploaded_file.name.split('.')[-1].lower()
        self.logger.info(f"Processing file: {uploaded_file.name} (type: {file_extension})")
        
        try:
            if file_extension == 'csv':
                return self._process_csv(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                return self._process_excel(uploaded_file)
            elif file_extension == 'txt':
                return self._process_text(uploaded_file)
            elif file_extension == 'pdf':
                return self._process_pdf(uploaded_file)
            elif file_extension in ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif']:
                return self._process_image(uploaded_file)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
                
        except Exception as e:
            self.logger.error(f"Error processing file {uploaded_file.name}: {str(e)}")
            raise
    
    def _process_csv(self, uploaded_file) -> pd.DataFrame:
        """Process CSV files"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    uploaded_file.seek(0)  # Reset file pointer
                    df = pd.read_csv(uploaded_file, encoding=encoding)
                    self.logger.info(f"CSV loaded successfully with encoding: {encoding}")
                    return df
                except UnicodeDecodeError:
                    continue
            
            raise ValueError("Unable to decode CSV file with common encodings")
            
        except Exception as e:
            raise ValueError(f"Error reading CSV: {str(e)}")
    
    def _process_excel(self, uploaded_file) -> pd.DataFrame:
        """Process Excel files"""
        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            self.logger.info("Excel file loaded successfully")
            return df
        except Exception as e:
            raise ValueError(f"Error reading Excel file: {str(e)}")
    
    def _process_text(self, uploaded_file) -> str:
        """Process text files"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    uploaded_file.seek(0)
                    content = uploaded_file.read().decode(encoding)
                    self.logger.info(f"Text file loaded with encoding: {encoding}")
                    return content
                except UnicodeDecodeError:
                    continue
            
            raise ValueError("Unable to decode text file")
            
        except Exception as e:
            raise ValueError(f"Error reading text file: {str(e)}")
    
    def _process_pdf(self, uploaded_file) -> str:
        """Process PDF files"""
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                text = ''
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\\n'
            
            if not text.strip():
                raise ValueError("No text could be extracted from PDF")
                
            self.logger.info(f"PDF processed successfully, extracted {len(text)} characters")
            return text
            
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")
    
    def _process_image(self, uploaded_file) -> str:
        """Process image files using OCR"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
            
            try:
                # Open image and extract text
                image = Image.open(tmp_file_path)
                extracted_text = pytesseract.image_to_string(image)
                
                if not extracted_text.strip():
                    raise ValueError("No text could be extracted from image")
                
                self.logger.info(f"Image processed successfully, extracted {len(extracted_text)} characters")
                return extracted_text
                
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)
                
        except pytesseract.TesseractNotFoundError:
            raise ValueError("Tesseract OCR not found. Please install Tesseract OCR.")
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")
    
    def generate_eda_report(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate Exploratory Data Analysis report for DataFrame
        
        Args:
            data: pandas DataFrame
            
        Returns:
            Dictionary containing EDA results
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("EDA can only be generated for tabular data (CSV/Excel)")
        
        report = {
            'summary': {},
            'plots': {}
        }
        
        try:
            # Basic info
            report['summary']['shape'] = data.shape
            report['summary']['columns'] = list(data.columns)
            report['summary']['dtypes'] = data.dtypes.to_dict()
            report['summary']['missing_values'] = data.isnull().sum().to_dict()
            
            # Statistical summary for numeric columns
            numeric_columns = data.select_dtypes(include=['number']).columns
            if len(numeric_columns) > 0:
                report['summary']['statistics'] = data[numeric_columns].describe().to_dict()
                
                # Generate plots
                plots_dir = os.path.join('data', 'outputs')
                os.makedirs(plots_dir, exist_ok=True)
                
                # Distribution plots for numeric columns
                for col in numeric_columns:
                    if data[col].nunique() > 1:  # Skip constant columns
                        plt.figure(figsize=(8, 6))
                        sns.histplot(data[col], kde=True)
                        plt.title(f'Distribution of {col}')
                        plot_path = os.path.join(plots_dir, f'{col}_distribution.png')
                        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                        plt.close()
                        report['plots'][f'{col}_distribution'] = plot_path
                
                # Correlation heatmap
                if len(numeric_columns) > 1:
                    plt.figure(figsize=(10, 8))
                    correlation_matrix = data[numeric_columns].corr()
                    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
                    plt.title('Correlation Heatmap')
                    plot_path = os.path.join(plots_dir, 'correlation_heatmap.png')
                    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                    plt.close()
                    report['plots']['correlation_heatmap'] = plot_path
            
            self.logger.info("EDA report generated successfully")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating EDA report: {str(e)}")
            raise
    
    def get_data_summary(self, data: Union[pd.DataFrame, str]) -> str:
        """
        Get a brief summary of the data for AI agent context
        
        Args:
            data: Processed data (DataFrame or string)
            
        Returns:
            String summary of the data
        """
        if isinstance(data, pd.DataFrame):
            summary = f"Dataset with {data.shape[0]} rows and {data.shape[1]} columns.\\n"
            summary += f"Columns: {', '.join(data.columns.tolist())}\\n"
            
            # Sample of the data
            if len(data) > 5:
                summary += f"\\nFirst 5 rows:\\n{data.head().to_string()}\\n"
            else:
                summary += f"\\nData preview:\\n{data.to_string()}\\n"
            
            # Basic statistics for numeric columns
            numeric_cols = data.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                summary += f"\\nBasic statistics for numeric columns:\\n"
                summary += data[numeric_cols].describe().to_string()
        
        elif isinstance(data, str):
            summary = f"Text data with {len(data)} characters.\\n"
            summary += f"Preview: {data[:500]}{'...' if len(data) > 500 else ''}"
        
        else:
            summary = "Unknown data type"
        
        return summary
