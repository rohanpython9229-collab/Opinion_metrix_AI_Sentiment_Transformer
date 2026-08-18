from src.database import engine
from src.models import ReviewPrediction


# Create a sample sentiment prediction record
# This is only for testing the PostgreSQL connection
test_record = ReviewPrediction(
    review="This is a test review for PostgreSQL.",
    sentiment="Positive",
    confidence=0.95
)


# Insert the test record into the review_predictions table
with engine.begin() as connection:
    connection.execute(
        ReviewPrediction.__table__.insert(),
        [{
            "review": test_record.review,
            "sentiment": test_record.sentiment,
            "confidence": test_record.confidence
        }]
    )


# Confirmation message
print("Test prediction inserted successfully!")
