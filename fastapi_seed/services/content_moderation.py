import logging
import time
from collections import deque
from threading import Lock
from typing import Dict, Optional

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ContentModerationService:
    _instance: Optional["ContentModerationService"] = None
    _initialized: bool = False

    # Mapping of model labels to human-readable categories
    CATEGORY_MAPPING = {
        "H": "Hate Speech",
        "H2": "Hate Speech (Severe)",
        "HR": "Hate Speech (Racial)",
        "OK": "Safe Content",
        "S": "Sexual Content",
        "S3": "Sexual Content (Explicit)",
        "SH": "Sexual Harassment",
        "V": "Violence",
        "V2": "Violence (Severe)"
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model_name: str = "KoalaAI/Text-Moderation"):
        if not self._initialized:
            self.model_name = model_name
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.eval()  # Set to evaluation mode

            # Request tracking
            self.request_times = deque(maxlen=1000)  # Store last 1000 requests
            self.lock = Lock()
            self._initialized = True
            logger.info("ContentModerationService initialized with model: %s", model_name)

    @classmethod
    def initialize(cls, model_name: str = "KoalaAI/Text-Moderation") -> "ContentModerationService":
        """Initialize the service and download the model."""
        return cls(model_name)

    def get_request_rate(self) -> float:
        """Calculate requests per second based on the last minute of requests."""
        current_time = time.time()
        one_minute_ago = current_time - 60

        with self.lock:
            # Remove old requests
            while self.request_times and self.request_times[0] < one_minute_ago:
                self.request_times.popleft()

            # Calculate rate
            if not self.request_times:
                return 0.0

            rate = len(self.request_times) / 60.0
            logger.info("Current request rate: %.2f requests/second", rate)
            return rate

    def moderate_text(self, text: str) -> Dict[str, float]:
        """Process text through the moderation model and return category scores."""
        # Track request
        with self.lock:
            self.request_times.append(time.time())

        # Tokenize and prepare input
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.sigmoid(outputs.logits).squeeze().numpy()

        # Get category labels and map them to human-readable categories
        labels = self.model.config.id2label

        # Create result dictionary with mapped categories
        result = {
            self.CATEGORY_MAPPING.get(labels[i], labels[i]): float(score)
            for i, score in enumerate(scores)
        }

        return result
