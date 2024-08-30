import spacy
import streamlit as st
from textblob import TextBlob

# Check if the spaCy model is available
model_name = 'en_core_web_sm'
try:
    nlp = spacy.load(model_name)
except OSError:
    st.error(f"Model '{model_name}' is not installed. Please run 'python -m spacy download {model_name}' to install it.")


# Function to analyze sentiment using TextBlob
def analyze_sentiment(review_text):
    blob = TextBlob(review_text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive", polarity
    elif polarity < 0:
        return "negative", polarity
    else:
        return "neutral", polarity

# Function to perform aspect-based sentiment analysis
def aspect_based_sentiment_analysis(review_text):
    doc = nlp(review_text)
    aspects = {"product_quality": "neutral", "delivery": "neutral", "customer_service": "neutral"}
    for token in doc:
        if token.text.lower() in ["quality", "product"]:
            aspects["product_quality"] = "positive" if token.sentiment > 0 else "negative"
        elif token.text.lower() in ["delivery", "shipping"]:
            aspects["delivery"] = "positive" if token.sentiment > 0 else "negative"
        elif token.text.lower() in ["service", "support"]:
            aspects["customer_service"] = "positive" if token.sentiment > 0 else "negative"
    return aspects

# Function to extract key phrases
def extract_key_phrases(review_text):
    doc = nlp(review_text)
    key_phrases = [chunk.text for chunk in doc.noun_chunks]
    return key_phrases

# Streamlit Interface
st.title("Customer Review Analysis")

review_text = st.text_area("Enter the customer review:")
review_rating = st.number_input("Enter the rating (optional):", min_value=1, max_value=5, step=1)

if st.button("Analyze Review"):
    # Perform analysis
    overall_sentiment, polarity = analyze_sentiment(review_text)
    aspect_sentiments = aspect_based_sentiment_analysis(review_text)
    key_phrases = extract_key_phrases(review_text)

    # Inferred rating if not provided
    if not review_rating:
        inferred_rating = int((polarity + 1) * 2.5)
    else:
        inferred_rating = review_rating

    # Display results
    st.subheader("Analysis Results:")
    st.write(f"**Overall Sentiment:** {overall_sentiment}")
    st.write(f"**Aspect Sentiments:** {aspect_sentiments}")
    st.write(f"**Key Phrases:** {', '.join(key_phrases)}")
    st.write(f"**Inferred Rating:** {inferred_rating}")

    # Display JSON-like response
    response = {
        "overall_sentiment": overall_sentiment,
        "aspect_sentiments": aspect_sentiments,
        "key_phrases": key_phrases,
        "inferred_rating": inferred_rating
    }
    st.json(response)
