# Import Hugging Face classes for loading the tokenizer and trained model
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Import PyTorch for model inference
import torch


# Hugging Face Hub model ID
MODEL_ID = "rohanpython9229/OpinionAI-Sentiment-DistilBERT"


# Limit CPU threads to reduce unnecessary memory usage
# This is useful for low-memory deployment environments such as Render.
torch.set_num_threads(1)


# Load the tokenizer used to convert text into model-compatible tokens
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)


# Load the fine-tuned DistilBERT model.
# low_cpu_mem_usage=True helps reduce peak RAM usage while loading.
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_ID,
    low_cpu_mem_usage=True
)

# Convert supported model layers to INT8 to reduce memory usage
model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8
)


# Put the model into evaluation mode.
# This disables training-specific behavior such as dropout.
model.eval()


# Confirmation message
print("OpinionAI model loaded successfully!")


def predict_sentiment(text: str) -> dict:
    """
    Predict the sentiment of a given review.

    Args:
        text (str): Input product review.

    Returns:
        dict: Predicted sentiment and confidence score.
    """

    # Validate the input
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Review text cannot be empty.")

    # Remove unnecessary spaces from the beginning and end
    text = text.strip()


    # Convert the review into tokens that DistilBERT understands.
    # padding=False avoids unnecessary padding for a single review.
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=False,
        max_length=128
    )


    # Run inference without creating gradients.
    # inference_mode is optimized for prediction-only workloads.
    with torch.inference_mode():
        outputs = model(**inputs)


    # Convert model logits into probabilities
    probabilities = torch.softmax(
        outputs.logits,
        dim=-1
    )


    # Get the class with the highest probability
    predicted_class = torch.argmax(
        probabilities,
        dim=-1
    ).item()


    # Get the confidence of the predicted class
    confidence = probabilities[
        0,
        predicted_class
    ].item()


    # Convert class ID into the sentiment name
    sentiment = model.config.id2label[
        predicted_class
    ]


    # Return sentiment and confidence
    return {
        "sentiment": sentiment,
        "confidence": round(confidence, 4)
    }
