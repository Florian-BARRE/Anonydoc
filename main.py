# ====== Code Summary ======
# This script initializes and runs the AnonyDoc application, which likely processes text documents for anonymization.
# It loads configuration values, initializes an entity processor for handling named entity recognition (NER),
# and starts the UI using Streamlit.

# ====== Third-Party Library Imports ======
import streamlit as st

# ====== Internal Project Imports ======
from config_loader import CONFIG
from entipy import TextEntityProcessor
from ui import AnonyDocApp


@st.cache_resource
def load_entity_processor() -> TextEntityProcessor:
    """
    Loads and caches the TextEntityProcessor instance with predefined configuration values.

    Returns:
        TextEntityProcessor: An initialized and cached text entity processor.
    """
    # Instantiate TextEntityProcessor using configuration values from CONFIG
    return TextEntityProcessor(
        model_name=CONFIG.GLINER_MODEL_NAME,
        context_window=CONFIG.GLINER_CONTEXT_WINDOW,
        threshold=CONFIG.GLINER_THRESHOLD,
    )


if __name__ == "__main__":
    # Initialize the AnonyDocApp with the cached text entity processor
    app = AnonyDocApp(
        text_entity_processor=load_entity_processor(),
    )
    # Run the AnonyDoc application
    app.run()
