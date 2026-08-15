# Import FastAPI to create our API application
from fastapi import FastAPI

# Import BaseModel for validating JSON request data
from pydantic import BaseModel

# Import our reusable sentiment prediction function
from src.inference import predict_sentiment


# Create the FastAPI application
app = FastAPI(
    title="OpinionAI Sentiment API",
    description="API for sentiment analysis using OpinionAI DistilBERT",
    version="1.0.0"
)


# Define the structure of the incoming JSON request
class ReviewRequest(BaseModel):
    review: str


# Root endpoint — checks whether the API is running
@app.get("/")
def root():
    return {
        "message": "OpinionAI Sentiment API is running!"
    }


# Sentiment prediction endpoint
@app.post("/predict")
def predict(request: ReviewRequest):
    """
    Predict the sentiment of a product review.

    Expected JSON:
    {
        "review": "This product is amazing!"
    }
    """

    # Send the review to our inference pipeline
    result = predict_sentiment(request.review)

    # Return sentiment and confidence as JSON
    return result
```
