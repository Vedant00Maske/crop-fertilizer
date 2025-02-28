import streamlit as st
import pickle
import numpy as np
from googletrans import Translator
from geminiService import get_fertilizer_strategy

# Load models
model = pickle.load(open('classifier.pkl', 'rb'))
ferti = pickle.load(open('fertilizer.pkl', 'rb'))

# Initialize Translator
translator = Translator()

# Language Selection
languages = {"English": "en", "Hindi": "hi", "Telugu": "te"}
selected_lang = st.sidebar.selectbox("Choose Language", list(languages.keys()))

def translate_text(text):
    return translator.translate(text, dest=languages[selected_lang]).text

# Custom CSS for the app
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2C3930;
        color: white;
    }
    .stButton>button {
        background-color: #A27B5C;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #8B6B4F;
    }
    .stSidebar {
        background-color: #3F4F44;
    }
    .stSidebar .stNumberInput input {
        background-color: #2C3930;
        color: white;
    }
    .stSidebar .stSelectbox select {
        background-color: #2C3930;
        color: white;
    }

    .stSidebar .stSlider > div > div > div > div {
        background: #9DC08B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit UI
st.title(translate_text("Plant Fertilizer Prediction"))
st.write(translate_text("This app predicts the type of fertilizer to be used for a particular crop based on the environmental conditions."))
# Add a video to the app
st.image("crop_fertilizer.jpg", width=500)
st.sidebar.header(translate_text("Input Parameters"))

# Input fields using sliders
temp = st.sidebar.slider(translate_text("Temperature"), min_value=0, max_value=100, value=25)
humi = st.sidebar.slider(translate_text("Humidity"), min_value=0, max_value=100, value=50)
mois = st.sidebar.slider(translate_text("Moisture"), min_value=0, max_value=100, value=30)
soil = st.sidebar.slider(translate_text("Soil Type (Numeric)"), min_value=0, max_value=10, value=1)
crop = st.sidebar.slider(translate_text("Crop Type (Numeric)"), min_value=0, max_value=10, value=1)
nitro = st.sidebar.slider(translate_text("Nitrogen Level"), min_value=0, max_value=100, value=20)
pota = st.sidebar.slider(translate_text("Potassium Level"), min_value=0, max_value=100, value=20)
phosp = st.sidebar.slider(translate_text("Phosphorus Level"), min_value=0, max_value=100, value=20)

# Prediction button
if st.sidebar.button(translate_text("Predict Fertilizer")):
    input_data = np.array([temp, humi, mois, soil, crop, nitro, pota, phosp]).reshape(1, -1)
    prediction = ferti.classes_[model.predict(input_data)][0]
    
    st.subheader(translate_text("Prediction:"))
    st.markdown(
        f"""
        <div style="background-color: #3F4F44; padding: 10px; border-radius: 5px;">
            <h3 style="color: #9DC08B;">{translate_text('The recommended fertilizer is')}: {translate_text(prediction)}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.spinner(translate_text("Fetching best strategies for using this fertilizer...")):
        strategy = get_fertilizer_strategy(prediction)

    st.subheader(translate_text("Usage Strategy:"))
    st.markdown(
        f"""
        <div style="background-color: #2C3930; padding: 15px; border-radius: 10px; margin-top: 10px; border: 1px solid #A27B5C;">
            <p style="color: white;">{translate_text(strategy)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )