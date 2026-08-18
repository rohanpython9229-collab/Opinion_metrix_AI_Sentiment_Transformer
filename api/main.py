# Import FastAPI to create our API application
from fastapi import FastAPI

# Import BaseModel for validating JSON request data
from pydantic import BaseModel

# Import our reusable sentiment prediction function
from src.inference import predict_sentiment

# Import database engine and database model
from src.database import engine
from src.models import ReviewPrediction

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
    Predict the sentiment of a product review
    and save the prediction to PostgreSQL.

    Expected JSON:
    {
        "review": "This product is amazing!"
    }
    """

    # Send the review to our inference pipeline
    result = predict_sentiment(request.review)

    # Create a database record using the prediction result
    prediction_record = ReviewPrediction(
        review=request.review,
        sentiment=result["sentiment"],
        confidence=result["confidence"]
    )

    # Save the prediction to PostgreSQL
    with engine.begin() as connection:
        connection.execute(
            ReviewPrediction.__table__.insert(),
            [{
                "review": prediction_record.review,
                "sentiment": prediction_record.sentiment,
                "confidence": prediction_record.confidence
            }]
        )

    # Return sentiment and confidence as JSON
    return result

