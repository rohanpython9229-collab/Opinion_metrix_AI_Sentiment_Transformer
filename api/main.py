# Import FastAPI to create our API application
from fastapi import FastAPI

# Import our trained model's prediction function
from src.inference import predict_sentiment


# Create the FastAPI application
app = FastAPI(
    title="OpinionAI Sentiment API",
    description="API for sentiment analysis using OpinionAI DistilBERT",
    version="1.0.0"
)


# Root endpoint — checks whether the API is running
@app.get("/")
def root():
    return {
        "message": "OpinionAI Sentiment API is running!"
    }


# Sentiment prediction endpoint
@app.post("/predict")
def predict(review: str):
    """
    Analyze the sentiment of a product review.

    Args:
        review: Product review text.

    Returns:
        Sentiment and confidence score.
    """

    # Use our reusable inference function
    result = predict_sentiment(review)

    # Return the prediction as an API response
    return result