import streamlit as st
import requests
import os
import time


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OpinionAI | Sentiment Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# FASTAPI CONFIGURATION
# ============================================================

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/predict"
)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "review" not in st.session_state:
    st.session_state.review = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "analyze_requested" not in st.session_state:
    st.session_state.analyze_requested = False


# ============================================================
# CALLBACK FUNCTIONS
# ============================================================

def set_positive_example():
    """Load a positive example and trigger analysis."""
    st.session_state.review = (
        "This product is amazing and works perfectly!"
    )
    st.session_state.analyze_requested = True


def set_neutral_example():
    """Load a neutral example and trigger analysis."""
    st.session_state.review = (
        "The product is okay. It works as expected."
    )
    st.session_state.analyze_requested = True


def set_negative_example():
    """Load a negative example and trigger analysis."""
    st.session_state.review = (
        "The product is terrible and stopped working."
    )
    st.session_state.analyze_requested = True


def clear_review():
    """Clear the review and previous prediction."""
    st.session_state.review = ""
    st.session_state.last_result = None
    st.session_state.analyze_requested = False


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    /* Subtitle */
    .main-subtitle {
        text-align: center;
        font-size: 1.05rem;
        opacity: 0.65;
        margin-bottom: 2.5rem;
    }

    /* Section heading */
    .section-heading {
        font-size: 1.35rem;
        font-weight: 750;
        margin-bottom: 0.8rem;
    }

    /* Sidebar cards */
    .sidebar-card {
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-radius: 12px;
        padding: 0.9rem;
        margin-bottom: 0.8rem;
    }

    .sidebar-title {
        font-weight: 700;
        font-size: 0.95rem;
    }

    .sidebar-value {
        opacity: 0.7;
        margin-top: 0.2rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        opacity: 0.5;
        font-size: 0.82rem;
    }

    /* Review text area */
    textarea {
        font-size: 1.25rem !important;
        line-height: 1.6 !important;
        padding: 1rem !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 OpinionAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'AI-Powered Sentiment Analysis using Transformer Models'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ About OpinionAI")

    st.write(
        "OpinionAI analyzes customer reviews and "
        "classifies them into Positive, Neutral, "
        "or Negative sentiment."
    )

    st.divider()

    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    st.subheader("🧠 Model")

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Transformer</div>
            <div class="sidebar-value">DistilBERT</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Backend
    # --------------------------------------------------------

    st.subheader("🚀 Backend")

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">API Framework</div>
            <div class="sidebar-value">FastAPI</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    st.subheader("🗄️ Database")

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Database</div>
            <div class="sidebar-value">PostgreSQL • Aiven</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("OpinionAI v1.0")
    st.caption("Transformer-based Sentiment Analysis")


# ============================================================
# MAIN TWO-COLUMN LAYOUT
# ============================================================

left_col, right_col = st.columns(
    [1.1, 0.9],
    gap="large"
)


# ============================================================
# LEFT COLUMN — REVIEW INPUT
# ============================================================

with left_col:

    st.markdown(
        '<div class="section-heading">💬 Analyze a Review</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Review input
    # --------------------------------------------------------

    st.text_area(
        "Review",
        height=220,
        placeholder=(
            "Example:\n"
            "This product is amazing and works perfectly!"
        ),
        label_visibility="collapsed",
        key="review"
    )

    # --------------------------------------------------------
    # Character counter
    # --------------------------------------------------------

    character_count = len(
        st.session_state.review
    )

    st.caption(
        f"📝 Characters: {character_count}"
    )

    # ========================================================
    # EXAMPLE REVIEWS
    # ========================================================

    st.markdown(
        '<div class="section-heading">✨ Try an Example</div>',
        unsafe_allow_html=True
    )

    example_col1, example_col2, example_col3 = st.columns(3)

    # --------------------------------------------------------
    # Positive
    # --------------------------------------------------------

    with example_col1:

        st.button(
            "😊 Positive",
            use_container_width=True,
            key="positive_example",
            on_click=set_positive_example
        )

    # --------------------------------------------------------
    # Neutral
    # --------------------------------------------------------

    with example_col2:

        st.button(
            "😐 Neutral",
            use_container_width=True,
            key="neutral_example",
            on_click=set_neutral_example
        )

    # --------------------------------------------------------
    # Negative
    # --------------------------------------------------------

    with example_col3:

        st.button(
            "😞 Negative",
            use_container_width=True,
            key="negative_example",
            on_click=set_negative_example
        )

    st.write("")

    # ========================================================
    # ACTION BUTTONS
    # ========================================================

    action_col1, action_col2 = st.columns(
        [3, 1]
    )

    # --------------------------------------------------------
    # Analyze
    # --------------------------------------------------------

    with action_col1:

        analyze_clicked = st.button(
            "🔍 Analyze Sentiment",
            type="primary",
            use_container_width=True,
            key="analyze_button"
        )

    # --------------------------------------------------------
    # Clear
    # --------------------------------------------------------

    with action_col2:

        st.button(
            "🗑️ Clear",
            use_container_width=True,
            key="clear_button",
            on_click=clear_review
        )


# ============================================================
# ANALYSIS TRIGGER
# ============================================================

should_analyze = (
    analyze_clicked
    or st.session_state.analyze_requested
)


# ============================================================
# FASTAPI REQUEST
# ============================================================

if should_analyze:

    # Reset automatic example trigger
    st.session_state.analyze_requested = False

    # --------------------------------------------------------
    # Empty review
    # --------------------------------------------------------

    if not st.session_state.review.strip():

        st.session_state.last_result = None

        st.warning(
            "⚠️ Please enter a review before analyzing."
        )

    else:

        try:

            # ------------------------------------------------
            # Send request to FastAPI with retry mechanism
            # ------------------------------------------------

            with st.spinner(
                "🤖 OpinionAI is analyzing your review..."
            ):

                response = None

                for attempt in range(12):

                    try:

                        response = requests.post(
                            API_URL,
                            json={
                                "review": st.session_state.review
                            },
                            timeout=30
                        )

                        # Request reached FastAPI.
                        # Stop retrying regardless of HTTP status.
                        break

                    except requests.exceptions.ConnectionError:

                        if attempt == 11:
                            raise

                        time.sleep(5)

            # ------------------------------------------------
            # Successful response
            # ------------------------------------------------

            if response.status_code == 200:

                st.session_state.last_result = (
                    response.json()
                )

            # ------------------------------------------------
            # API returned an error
            # ------------------------------------------------

            else:

                st.session_state.last_result = {
                    "error": (
                        f"API returned status code "
                        f"{response.status_code}"
                    )
                }

        # ----------------------------------------------------
        # FastAPI is not running
        # ----------------------------------------------------

        except requests.exceptions.ConnectionError:

            st.session_state.last_result = {
                "error": (
                    "FastAPI connection failed.\n\n"
                    "The API could not be reached after "
                    "multiple attempts. Please try again."
                )
            }

        # ----------------------------------------------------
        # Request timeout
        # ----------------------------------------------------

        except requests.exceptions.Timeout:

            st.session_state.last_result = {
                "error": (
                    "Request timed out.\n\n"
                    "Please try again."
                )
            }

        # ----------------------------------------------------
        # Unexpected error
        # ----------------------------------------------------

        except Exception as e:

            st.session_state.last_result = {
                "error": f"Unexpected error: {e}"
            }


# ============================================================
# RIGHT COLUMN — ANALYSIS RESULT
# ============================================================

with right_col:

    st.markdown(
        '<div class="section-heading">📊 Analysis Result</div>',
        unsafe_allow_html=True
    )

    result = st.session_state.last_result

    # ========================================================
    # NO RESULT
    # ========================================================

    if result is None:

        with st.container(border=True):

            st.markdown("### 👋 Ready to analyze")

            st.write(
                "Enter a customer review on the left "
                "and click **Analyze Sentiment**."
            )

            st.info(
                "💡 You can also try one of the "
                "example reviews."
            )

    # ========================================================
    # ERROR
    # ========================================================

    elif "error" in result:

        with st.container(border=True):

            st.error(
                result["error"]
            )

    # ========================================================
    # SUCCESSFUL RESULT
    # ========================================================

    else:

        # ----------------------------------------------------
        # Extract result
        # ----------------------------------------------------

        sentiment = str(
            result.get(
                "sentiment",
                "Unknown"
            )
        ).upper()

        confidence = float(
            result.get(
                "confidence",
                0
            )
        )

        # ----------------------------------------------------
        # Convert confidence to percentage
        # ----------------------------------------------------

        if confidence <= 1:

            confidence_percent = (
                confidence * 100
            )

        else:

            confidence_percent = confidence

        # ----------------------------------------------------
        # Sentiment information
        # ----------------------------------------------------

        if sentiment == "POSITIVE":

            emoji = "😊"
            message = "Positive opinion detected!"

        elif sentiment == "NEGATIVE":

            emoji = "😞"
            message = "Negative opinion detected!"

        elif sentiment == "NEUTRAL":

            emoji = "😐"
            message = "Neutral opinion detected!"

        else:

            emoji = "🤖"
            message = "Sentiment detected."

        # ====================================================
        # MAIN RESULT CARD
        # ====================================================

        with st.container(border=True):

            st.markdown(
                "### 🎯 Detected Sentiment"
            )

            st.markdown(
                f"# {emoji} {sentiment}"
            )

            st.divider()

            # ------------------------------------------------
            # Confidence
            # ------------------------------------------------

            st.markdown(
                "#### 🎯 Model Confidence"
            )

            st.progress(
                min(
                    confidence_percent / 100,
                    1.0
                )
            )

            st.markdown(
                f"**{confidence_percent:.2f}%**"
            )

        st.write("")

        # ====================================================
        # SENTIMENT MESSAGE
        # ====================================================

        if sentiment == "POSITIVE":

            st.success(
                f"🎉 {message}"
            )

        elif sentiment == "NEGATIVE":

            st.error(
                f"⚠️ {message}"
            )

        elif sentiment == "NEUTRAL":

            st.info(
                f"ℹ️ {message}"
            )

        else:

            st.warning(
                f"🤖 {message}"
            )

        st.write("")

        # ====================================================
        # PREDICTION DETAILS
        # ====================================================

        st.markdown(
            "### 🔎 Prediction Details"
        )

        detail_col1, detail_col2 = st.columns(2)

        with detail_col1:

            st.metric(
                label="Sentiment",
                value=sentiment
            )

        with detail_col2:

            st.metric(
                label="Confidence",
                value=f"{confidence_percent:.2f}%"
            )

        st.caption(
            "✓ Prediction generated by the "
            "OpinionAI DistilBERT model."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    'OpinionAI • DistilBERT • FastAPI • PostgreSQL • Aiven'
    '</div>',
    unsafe_allow_html=True
)
