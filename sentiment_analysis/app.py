import streamlit as st
import pickle
import re

# Load model
with open("model/sentiment_model.pkl", "rb") as f:
    model = pickle.load(f)

# Load vectorizer
with open("model/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


# Clean text function
def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z\s]",
        "",
        text
    )

    return text


# Sentiment prediction
def analyze_sentiment(review):

    cleaned_review = clean_text(review)

    review_vectorized = vectorizer.transform(
        [cleaned_review]
    )

    prediction = model.predict(
        review_vectorized
    )

    probability = model.predict_proba(
        review_vectorized
    )

    positive_prob = probability[0][1] * 100

    return prediction[0], positive_prob


# Streamlit UI
st.title("AI Sentiment Analysis Dashboard")

st.sidebar.title("About")

st.sidebar.write(
    "AI-powered sentiment analysis system"
)

st.sidebar.write(
    "Model Accuracy: 89%"
)

# User input
user_input = st.text_area(
    "Enter a Review"
)

# Analyze button
if st.button("Analyze Sentiment"):

    if user_input:

        prediction, positive_prob = analyze_sentiment(
            user_input
        )

        # Metrics
        col1, col2 = st.columns(2)

        col1.metric(
            "Model Accuracy",
            "89%"
        )

        col2.metric(
            "Positive Score",
            f"{positive_prob:.1f}%"
        )

        # Prediction
        if prediction == 1:

            st.success(
                "Positive Sentiment"
            )

        else:

            st.error(
                "Negative Sentiment"
            )

        # Probability
        st.write(
            f"Positive Sentiment Probability: {positive_prob:.2f}%"
        )

        st.progress(
            int(positive_prob)
        )

        # Sentiment strength
        if positive_prob > 80:

            st.success(
                "Strong Positive Review"
            )

        elif positive_prob > 60:

            st.info(
                "Moderately Positive Review"
            )

        elif positive_prob > 40:

            st.warning(
                "Neutral/Mixed Review"
            )

        else:

            st.error(
                "Strong Negative Review"
            )

        # Trigger words
        positive_words = [
            "amazing",
            "great",
            "excellent",
            "love",
            "fantastic",
            "best"
        ]

        negative_words = [
            "worst",
            "bad",
            "awful",
            "hate",
            "terrible",
            "boring",
            "horror"
        ]

        detected_positive = []

        detected_negative = []

        cleaned_input = clean_text(
            user_input
        )

        # Detect positive words
        for word in positive_words:

            if word in cleaned_input:

                detected_positive.append(word)

        # Detect negative words
        for word in negative_words:

            if word in cleaned_input:

                detected_negative.append(word)

        # Show positive keywords
        if len(detected_positive) > 0:

            st.write(
                "Positive Keywords:"
            )

            for word in detected_positive:

                st.write(f"- {word}")

        # Show negative keywords
        if len(detected_negative) > 0:

            st.write(
                "Negative Keywords:"
            )

            for word in detected_negative:

                st.write(f"- {word}")

        # Download report
        report = f"""
Sentiment Analysis Report

Review:
{user_input}

Positive Sentiment Probability:
{positive_prob:.2f}%
"""

        st.download_button(
            label="Download Report",
            data=report,
            file_name="sentiment_report.txt",
            mime="text/plain"
        )

    else:

        st.warning(
            "Please enter a review."
        )