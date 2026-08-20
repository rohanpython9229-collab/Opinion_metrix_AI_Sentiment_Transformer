# Import FastAPI to create the API
from fastapi import FastAPI

# Import FileResponse to serve the HTML frontend
from fastapi.responses import FileResponse

# Import BaseModel to validate request data
from pydantic import BaseModel

# Import the sentiment prediction function
from src.inference import predict_sentiment

# Import the database connection
from src.database import engine

# Import the database table model
from src.models import ReviewPrediction


# Create the FastAPI application
app = FastAPI(
    title="OpinionAI Sentiment API",
    description="API for sentiment analysis using OpinionAI DistilBERT",
    version="1.0.0"
)


# Define the format of the review request
class ReviewRequest(BaseModel):
    review: str


# Open the frontend when the user visits the main URL
@app.get("/", response_class=FileResponse)
def frontend():
    return FileResponse("frontend/index.html")


# Check if the API is running
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "OpinionAI API is running!"
    }


# Predict sentiment for a review
@app.post("/predict")
def predict(request: ReviewRequest):

    # Get sentiment prediction from the model
    result = predict_sentiment(request.review)

    # Create a database record
    prediction_record = ReviewPrediction(
        review=request.review,
        sentiment=result["sentiment"],
        confidence=result["confidence"]
    )

    # Save the review and prediction in PostgreSQL
    with engine.begin() as connection:
        connection.execute(
            ReviewPrediction.__table__.insert(),
            [{
                "review": prediction_record.review,
                "sentiment": prediction_record.sentiment,
                "confidence": prediction_record.confidence
            }]
        )

    # Return the prediction to the frontend
    return result