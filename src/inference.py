# Import Hugging Face classes for loading the tokenizer and trained model
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


# Hugging Face Hub par hamare fine-tuned sentiment model ka ID
MODEL_ID = "rohanpython9229/OpinionAI-Sentiment-DistilBERT"


# Load the tokenizer used to convert text into model-compatible tokens
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

# Load our fine-tuned DistilBERT sentiment classification model
model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)


# Put the model into evaluation mode
# This disables training-specific behavior such as dropout
model.eval()


# Confirmation message
print("OpinionAI model loaded successfully!")


def predict_sentiment(text: str) -> dict:
    """
    Predict the sentiment of a given review.

    Returns:
        dict: Predicted sentiment and confidence score.
    """

    # Convert the input review into tokens that DistilBERT understands
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    # Disable gradient calculation because we are only making predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Convert model logits into probabilities
    probabilities = torch.softmax(outputs.logits, dim=-1)

    # Get the class with the highest probability
    predicted_class = torch.argmax(probabilities, dim=-1).item()

    # Get the confidence of the predicted class
    confidence = probabilities[0][predicted_class].item()

    # Convert class ID (0/1/2) into the actual sentiment name
    sentiment = model.config.id2label[predicted_class]

    return {
        "sentiment": sentiment,
        "confidence": confidence
    }