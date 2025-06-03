import logging
import time
from collections import deque
from threading import Lock
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)

class RPSTrackerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        window_size: int = 60,  # Window size in seconds
        max_requests: int = 1000,  # Maximum number of requests to store
    ):
        super().__init__(app)
        self.window_size = window_size
        self.request_times = deque(maxlen=max_requests)
        self.lock = Lock()
        logger.info("RPS Tracker Middleware initialized with window size: %d seconds", window_size)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Record request time
        current_time = time.time()
        with self.lock:
            self.request_times.append(current_time)
            self._cleanup_old_requests(current_time)
            rps = self._calculate_rps(current_time)

        # Add RPS to request state for potential use in route handlers
        request.state.rps = rps

        # Process the request
        response = await call_next(request)

        # Log RPS after processing
        logger.info(
            "Request processed - Path: %s, Method: %s, RPS: %.2f",
            request.url.path,
            request.method,
            rps
        )

        return response

    def _cleanup_old_requests(self, current_time: float) -> None:
        """Remove requests older than the window size."""
        cutoff_time = current_time - self.window_size
        while self.request_times and self.request_times[0] < cutoff_time:
            self.request_times.popleft()

    def _calculate_rps(self, current_time: float) -> float:
        """Calculate requests per second based on the window size."""
        if not self.request_times:
            return 0.0

        # Calculate the actual time window
        window_start = self.request_times[0]
        window_duration = current_time - window_start

        if window_duration == 0:
            return 0.0

        return len(self.request_times) / window_duration
