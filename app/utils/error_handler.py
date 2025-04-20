from fastapi import HTTPException, status
from typing import Any, Dict, Optional
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StockAnalysisError(Exception):
    """Base exception for stock analysis related errors"""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class DataFetchError(StockAnalysisError):
    """Exception raised when there's an error fetching stock data"""
    def __init__(self, message: str, ticker: Optional[str] = None):
        super().__init__(message, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.ticker = ticker

class ValidationError(StockAnalysisError):
    """Exception raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)

def handle_error(error: Exception) -> Dict[str, Any]:
    """Handle exceptions and return appropriate error response"""
    if isinstance(error, StockAnalysisError):
        logger.error(f"Stock Analysis Error: {error.message}")
        return {
            "error": error.message,
            "status_code": error.status_code,
            "type": error.__class__.__name__
        }
    else:
        logger.error(f"Unexpected error: {str(error)}\n{traceback.format_exc()}")
        return {
            "error": "An unexpected error occurred",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "type": "UnexpectedError"
        } 