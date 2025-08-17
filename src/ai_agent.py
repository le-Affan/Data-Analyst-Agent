"""
AI Agent Module
Handles communication with Together AI's LLaMA model for data analysis
"""

import together
import os
import logging
import time
from typing import Union, Dict, Any
import pandas as pd
from data_processor import DataProcessor

class AIAgent:
    """AI Agent for data analysis using Together AI's LLaMA model"""
    
    def __init__(self, api_key: str, model: str = None, max_tokens: int = 500, temperature: float = 0.7):
        """
        Initialize the AI Agent
        
        Args:
            api_key: Together AI API key
            model: Model name to use
            max_tokens: Maximum tokens for response
            temperature: Temperature for response generation
        """
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key
        self.model = model or os.getenv("AI_MODEL", "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8")
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # Initialize Together client
        self.client = together.Together(api_key=api_key)
        self.data_processor = DataProcessor()
        
        # Test the connection
        self._test_connection()
    
    def _test_connection(self):
        """Test the AI model connection"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello, are you working?"}],
                max_tokens=50,
                temperature=0.7
            )
            self.logger.info("AI Agent connection successful")
        except Exception as e:
            self.logger.error(f"Failed to connect to AI model: {str(e)}")
            raise ValueError(f"AI Agent initialization failed: {str(e)}")
    
    def analyze_data(self, data: Union[pd.DataFrame, str], question: str, file_info: Dict[str, Any] = None) -> str:
        """
        Analyze data using AI and answer the user's question
        
        Args:
            data: Processed data (DataFrame or string)
            question: User's question about the data
            file_info: Information about the uploaded file
            
        Returns:
            AI-generated analysis response
        """
        try:
            # Prepare context for the AI
            context = self._prepare_context(data, file_info)
            
            # Create the prompt
            prompt = self._create_prompt(context, question)
            
            # Get AI response with retry logic
            response = self._get_ai_response(prompt)
            
            # Log the interaction
            self._log_interaction(question, response, file_info)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in data analysis: {str(e)}")
            raise
    
    def _prepare_context(self, data: Union[pd.DataFrame, str], file_info: Dict[str, Any] = None) -> str:
        """Prepare context information for the AI"""
        context = "You are a professional data analyst AI assistant. "
        
        if file_info:
            context += f"The user has uploaded a {file_info.get('type', 'file')} file named '{file_info.get('name', 'unknown')}'. "
        
        # Get data summary
        data_summary = self.data_processor.get_data_summary(data)
        context += f"\\n\\nData Summary:\\n{data_summary}\\n\\n"
        
        context += ("Please analyze this data and provide insights. "
                   "Be specific, accurate, and helpful. If you need to make assumptions, "
                   "clearly state them. Provide actionable insights when possible.")
        
        return context
    
    def _create_prompt(self, context: str, question: str) -> str:
        """Create a well-formatted prompt for the AI"""
        prompt = f"{context}\\n\\nUser Question: {question}\\n\\nPlease provide a detailed analysis:"
        return prompt
    
    def _get_ai_response(self, prompt: str, max_retries: int = 3) -> str:
        """
        Get response from AI with retry logic for rate limits
        
        Args:
            prompt: The prompt to send to AI
            max_retries: Maximum number of retries for rate limits
            
        Returns:
            AI response text
        """
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                error_str = str(e).lower()
                
                if "rate limit" in error_str and attempt < max_retries - 1:
                    wait_time = 60 * (attempt + 1)  # Exponential backoff
                    self.logger.warning(f"Rate limit hit, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    self.logger.error(f"AI API error: {str(e)}")
                    raise ValueError(f"Failed to get AI response: {str(e)}")
        
        raise ValueError("Max retries exceeded for AI API calls")
    
    def _log_interaction(self, question: str, response: str, file_info: Dict[str, Any] = None):
        """Log the interaction for future reference"""
        try:
            # Create logs directory if it doesn't exist
            logs_dir = "logs"
            os.makedirs(logs_dir, exist_ok=True)
            
            # Log to agent responses file
            with open(os.path.join(logs_dir, "agent_responses.txt"), "a", encoding='utf-8') as f:
                f.write(f"=== {time.strftime('%Y-%m-%d %H:%M:%S')} ===\\n")
                if file_info:
                    f.write(f"File: {file_info.get('name', 'unknown')} ({file_info.get('type', 'unknown')})\\n")
                f.write(f"Question: {question}\\n")
                f.write(f"Response: {response}\\n")
                f.write("=" * 60 + "\\n\\n")
            
            # Log to interaction log
            with open(os.path.join(logs_dir, "interaction_log.txt"), "a", encoding='utf-8') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | ")
                f.write(f"File: {file_info.get('name', 'N/A') if file_info else 'N/A'} | ")
                f.write(f"Question: {question[:100]}{'...' if len(question) > 100 else ''}\\n")
            
        except Exception as e:
            self.logger.error(f"Failed to log interaction: {str(e)}")
    
    def generate_summary_report(self, data: Union[pd.DataFrame, str], file_info: Dict[str, Any] = None) -> str:
        """
        Generate a comprehensive summary report of the data
        
        Args:
            data: Processed data
            file_info: File information
            
        Returns:
            Comprehensive data summary
        """
        summary_question = ("Please provide a comprehensive summary of this data including: "
                           "1. Overview of the data structure and content, "
                           "2. Key insights and patterns, "
                           "3. Notable trends or anomalies, "
                           "4. Potential business implications or recommendations, "
                           "5. Data quality assessment.")
        
        return self.analyze_data(data, summary_question, file_info)
    
    def suggest_questions(self, data: Union[pd.DataFrame, str], file_info: Dict[str, Any] = None) -> str:
        """
        Suggest relevant questions that can be asked about the data
        
        Args:
            data: Processed data
            file_info: File information
            
        Returns:
            List of suggested questions
        """
        suggestion_prompt = ("Based on this data, suggest 5-10 interesting and relevant questions "
                           "that would provide valuable insights. Focus on questions that would "
                           "help understand the data better, identify trends, or make business decisions.")
        
        return self.analyze_data(data, suggestion_prompt, file_info)
    
    def explain_column(self, data: pd.DataFrame, column_name: str, file_info: Dict[str, Any] = None) -> str:
        """
        Provide detailed analysis of a specific column
        
        Args:
            data: DataFrame containing the column
            column_name: Name of the column to analyze
            file_info: File information
            
        Returns:
            Detailed column analysis
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Column analysis is only available for structured data")
        
        if column_name not in data.columns:
            raise ValueError(f"Column '{column_name}' not found in data")
        
        question = (f"Please provide a detailed analysis of the '{column_name}' column, "
                   f"including its data distribution, summary statistics, patterns, "
                   f"potential issues, and insights.")
        
        return self.analyze_data(data, question, file_info)
