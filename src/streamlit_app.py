"""
Data Analyst Agent - Streamlit Application
A multi-modal AI-powered data analyst that processes various file types
"""

import streamlit as st
import os
from dotenv import load_dotenv
import sys
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent))

from data_processor import DataProcessor
from ai_agent import AIAgent
from utils import setup_logging, initialize_session_state

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🦾 Data Analyst Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar configuration
    with st.sidebar:
        st.title("🛠️ Configuration")
        
        # API Key management
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            api_key = st.text_input(
                "Together AI API Key", 
                type="password",
                help="Get your API key from https://api.together.xyz/"
            )
            if api_key:
                os.environ["TOGETHER_API_KEY"] = api_key
        else:
            st.success("✅ API Key loaded from environment")
        
        # Model settings
        st.subheader("🤖 Model Settings")
        model = st.selectbox(
            "AI Model",
            ["meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"],
            help="AI model for analysis"
        )
        
        max_tokens = st.slider("Max Tokens", 100, 1000, 500)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        
        # File upload settings
        st.subheader("📁 Upload Settings")
        max_file_size = st.number_input("Max File Size (MB)", 1, 100, 50)
    
    # Main interface
    st.title("🦾 Data Analyst Agent")
    st.markdown(
        """
        Welcome to the **Data Analyst Agent**! Upload your files and ask intelligent questions 
        about your data. Supports CSV, Excel, PDF, images, and text files.
        """
    )
    
    # Check if API key is available
    if not os.getenv("TOGETHER_API_KEY"):
        st.warning("⚠️ Please provide your Together AI API key in the sidebar to continue.")
        st.stop()
    
    # Initialize components
    try:
        data_processor = DataProcessor()
        ai_agent = AIAgent(
            api_key=os.getenv("TOGETHER_API_KEY"),
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )
    except Exception as e:
        st.error(f"❌ Failed to initialize components: {str(e)}")
        logger.error(f"Initialization error: {str(e)}")
        st.stop()
    
    # File upload section
    st.header("📤 Upload Your Data")
    
    uploaded_file = st.file_uploader(
        "Choose a file to analyze",
        type=['csv', 'xlsx', 'xls', 'txt', 'pdf', 'png', 'jpg', 'jpeg'],
        help="Supported formats: CSV, Excel, Text, PDF, Images"
    )
    
    if uploaded_file is not None:
        # Display file information
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 File Name", uploaded_file.name)
        with col2:
            st.metric("📏 File Size", f"{uploaded_file.size / 1024:.1f} KB")
        with col3:
            file_type = uploaded_file.name.split('.')[-1].upper()
            st.metric("🏷️ File Type", file_type)
        
        # Process the file
        try:
            with st.spinner("🔄 Processing file..."):
                processed_data = data_processor.process_file(uploaded_file)
                
                if processed_data:
                    st.session_state.processed_data = processed_data
                    st.session_state.file_info = {
                        'name': uploaded_file.name,
                        'type': file_type,
                        'size': uploaded_file.size
                    }
                    
                    st.success("✅ File processed successfully!")
                    
                    # Display data preview based on file type
                    display_data_preview(processed_data, file_type)
                    
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            logger.error(f"File processing error: {str(e)}")
    
    # Query interface
    if 'processed_data' in st.session_state:
        st.header("❓ Ask Questions About Your Data")
        
        # Text input for questions
        user_question = st.text_input(
            "💭 What would you like to know about your data?",
            placeholder="e.g., What are the main trends in this data?",
            key="question_input"
        )
        
        # Voice input section
        with st.expander("🎙️ Voice Input (Experimental)"):
            if st.button("🔴 Record Voice Question"):
                try:
                    voice_question = record_voice_input()
                    if voice_question:
                        st.session_state.question_input = voice_question
                        st.experimental_rerun()
                except Exception as e:
                    st.error(f"❌ Voice input error: {str(e)}")
        
        # Process question
        if user_question and st.button("🚀 Analyze", type="primary"):
            with st.spinner("🤔 Analyzing your question..."):
                try:
                    response = ai_agent.analyze_data(
                        st.session_state.processed_data,
                        user_question,
                        st.session_state.file_info
                    )
                    
                    # Display response
                    st.subheader("🤖 AI Analysis")
                    st.write(response)
                    
                    # Save to history
                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    
                    st.session_state.chat_history.append({
                        'question': user_question,
                        'response': response,
                        'file': st.session_state.file_info['name']
                    })
                    
                except Exception as e:
                    st.error(f"❌ Analysis error: {str(e)}")
                    logger.error(f"Analysis error: {str(e)}")
        
        # Chat history
        if 'chat_history' in st.session_state and st.session_state.chat_history:
            st.header("💬 Chat History")
            
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"💭 {chat['question'][:50]}..."):
                    st.write(f"**File:** {chat['file']}")
                    st.write(f"**Question:** {chat['question']}")
                    st.write(f"**Response:** {chat['response']}")
    
    # Additional features section
    if 'processed_data' in st.session_state:
        st.header("🔧 Additional Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Generate EDA Report"):
                generate_eda_report(st.session_state.processed_data, data_processor)
        
        with col2:
            if st.button("💾 Download Analysis"):
                download_analysis()

def display_data_preview(data, file_type):
    """Display preview of processed data"""
    st.subheader("👀 Data Preview")
    
    if file_type in ['CSV', 'XLSX', 'XLS']:
        st.dataframe(data.head(10))
        
        # Basic statistics
        if len(data.select_dtypes(include='number').columns) > 0:
            st.subheader("📈 Basic Statistics")
            st.dataframe(data.describe())
    
    elif file_type in ['TXT', 'PDF']:
        st.text_area("Text Content", data[:1000] + "..." if len(data) > 1000 else data)
    
    elif file_type in ['PNG', 'JPG', 'JPEG']:
        st.text_area("Extracted Text", data[:500] + "..." if len(data) > 500 else data)

def record_voice_input():
    """Record and process voice input"""
    # This would integrate with speech recognition
    # For now, return placeholder
    st.info("🎙️ Voice input feature coming soon!")
    return None

def generate_eda_report(data, processor):
    """Generate exploratory data analysis report"""
    try:
        with st.spinner("📊 Generating EDA report..."):
            report = processor.generate_eda_report(data)
            
            st.subheader("📊 Exploratory Data Analysis")
            
            # Display visualizations if available
            if 'plots' in report:
                for plot_name, plot_path in report['plots'].items():
                    if os.path.exists(plot_path):
                        st.image(plot_path, caption=plot_name)
            
            # Display summary statistics
            if 'summary' in report:
                st.write("**Summary Statistics:**")
                st.json(report['summary'])
                
    except Exception as e:
        st.error(f"❌ EDA generation error: {str(e)}")

def download_analysis():
    """Prepare analysis for download"""
    if 'chat_history' in st.session_state:
        # Create downloadable analysis report
        report_content = "# Data Analysis Report\n\n"
        
        for i, chat in enumerate(st.session_state.chat_history):
            report_content += f"## Question {i+1}\n"
            report_content += f"**File:** {chat['file']}\n"
            report_content += f"**Question:** {chat['question']}\n"
            report_content += f"**Response:** {chat['response']}\n\n"
        
        st.download_button(
            label="📥 Download Report",
            data=report_content,
            file_name="data_analysis_report.md",
            mime="text/markdown"
        )
    else:
        st.warning("⚠️ No analysis history to download")

if __name__ == "__main__":
    main()
