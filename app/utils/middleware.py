from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from app.utils.logging import log_info


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log request/response information."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        log_info(
            f"Request started",
            extra_data={
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host
            }
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        log_info(
            f"Request completed",
            extra_data={
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "process_time": f"{process_time:.3f}s"
            }
        )
        
        return response