"""
Utilities Module
Helper functions for logging, session management, and other utilities
"""

import logging
import os
import streamlit as st
from datetime import datetime
import json

def setup_logging(log_level: str = None):
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Get log level from environment or parameter
    level = log_level or os.getenv("LOG_LEVEL", "INFO")
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    # Configure logging
    logging.basicConfig(
        level=log_level_map.get(level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join("logs", "app.log"), encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # Suppress some noisy loggers
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    
    # Initialize session state variables if they don't exist
    session_vars = {
        'processed_data': None,
        'file_info': None,
        'chat_history': [],
        'eda_report': None,
        'current_analysis': None
    }
    
    for var, default_value in session_vars.items():
        if var not in st.session_state:
            st.session_state[var] = default_value

def validate_api_key(api_key: str) -> bool:
    """
    Validate if the API key looks correct
    
    Args:
        api_key: The API key to validate
        
    Returns:
        Boolean indicating if the key looks valid
    """
    if not api_key:
        return False
    
    # Basic validation - check if it's a reasonable length and format
    if len(api_key) < 20:
        return False
    
    # Check if it's not a placeholder
    if api_key in ["your_api_key_here", "your_together_ai_api_key_here"]:
        return False
    
    return True

def save_analysis_to_file(analysis_data: dict, filename: str = None):
    """
    Save analysis results to a JSON file
    
    Args:
        analysis_data: Dictionary containing analysis results
        filename: Optional filename, will generate one if not provided
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.json"
    
    # Create outputs directory if it doesn't exist
    output_dir = os.path.join("data", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False, default=str)
        return filepath
    except Exception as e:
        logging.error(f"Failed to save analysis to file: {str(e)}")
        raise

def load_analysis_from_file(filepath: str) -> dict:
    """
    Load analysis results from a JSON file
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Dictionary containing analysis results
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load analysis from file: {str(e)}")
        raise

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def get_file_type_emoji(file_extension: str) -> str:
    """
    Get emoji for file type
    
    Args:
        file_extension: File extension
        
    Returns:
        Emoji string
    """
    emoji_map = {
        'csv': '📊',
        'xlsx': '📈',
        'xls': '📈',
        'txt': '📝',
        'pdf': '📄',
        'png': '🖼️',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'bmp': '🖼️',
        'tiff': '🖼️',
        'gif': '🖼️'
    }
    
    return emoji_map.get(file_extension.lower(), '📄')

def create_download_link(data: str, filename: str, mime_type: str = "text/plain") -> str:
    """
    Create a download link for data
    
    Args:
        data: Data to download
        filename: Filename for download
        mime_type: MIME type for the file
        
    Returns:
        Download link HTML
    """
    import base64
    
    b64_data = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:{mime_type};base64,{b64_data}" download="{filename}">Download {filename}</a>'
    return href

def validate_file_type(filename: str, allowed_types: list) -> bool:
    """
    Validate if file type is allowed
    
    Args:
        filename: Name of the file
        allowed_types: List of allowed file extensions
        
    Returns:
        Boolean indicating if file type is valid
    """
    if not filename:
        return False
    
    file_extension = filename.split('.')[-1].lower()
    return file_extension in [ext.lower() for ext in allowed_types]

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not too long
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:96] + ext
    
    return filename

def get_system_info() -> dict:
    """
    Get system information for debugging
    
    Returns:
        Dictionary with system information
    """
    import platform
    import sys
    
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'python_version': sys.version,
        'working_directory': os.getcwd(),
        'timestamp': datetime.now().isoformat()
    }

def format_analysis_for_download(chat_history: list, file_info: dict = None) -> str:
    """
    Format chat history and analysis for download
    
    Args:
        chat_history: List of chat interactions
        file_info: Information about the analyzed file
        
    Returns:
        Formatted markdown string
    """
    content = "# Data Analysis Report\\n\\n"
    content += f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
    
    if file_info:
        content += "## File Information\\n\\n"
        content += f"- **File Name:** {file_info.get('name', 'N/A')}\\n"
        content += f"- **File Type:** {file_info.get('type', 'N/A')}\\n"
        content += f"- **File Size:** {format_file_size(file_info.get('size', 0))}\\n\\n"
    
    content += "## Analysis Results\\n\\n"
    
    for i, interaction in enumerate(chat_history, 1):
        content += f"### Question {i}\\n\\n"
        content += f"**Q:** {interaction.get('question', 'N/A')}\\n\\n"
        content += f"**A:** {interaction.get('response', 'N/A')}\\n\\n"
        content += "---\\n\\n"
    
    content += "\\n*Report generated by Data Analyst Agent*\\n"
    
    return content

class AnalysisCache:
    """Simple cache for analysis results to avoid redundant API calls"""
    
    def __init__(self, max_size: int = 50):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, key: str):
        """Get cached result"""
        return self.cache.get(key)
    
    def set(self, key: str, value: str):
        """Set cached result"""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[key] = value
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
    
    def create_key(self, data_summary: str, question: str) -> str:
        """Create cache key from data summary and question"""
        import hashlib
        
        key_string = f"{data_summary[:200]}_{question}"
        return hashlib.md5(key_string.encode()).hexdigest()
