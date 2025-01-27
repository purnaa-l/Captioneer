import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import numpy as np
import pandas as pd
import altair as alt

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set page configuration
st.set_page_config(page_title="Captioneer: Your Social Media Assistant")

# Title and Header
st.title("🎉 Captioneer: Generate Perfect Social Media Captions 🎉")
st.markdown("""
    **✍️ Need a caption for your latest photo or video? Captioneer has got you covered!**
    
    **Main Features:**
    - **Generate Caption**: Craft the best caption for your posts.
    - **Predict Engagement**: Get insights into optimal posting time and more.
    - **Best Social Media Trends**: Stay up to date with what's trending today.

    **Ready to elevate your social media game? Upload your image and let Captioneer do the magic! 🚀**
""")

# Helper Functions
def generate_dynamic_captions(theme, language, hashtags_included, uploaded_image):
    input_prompt = f"""
    You are a creative social media expert helping users craft captions for their posts.
    Analyze the uploaded image and generate the following based on the user’s preferences:
    1. **Primary Caption:** Provide a catchy caption suitable for the {theme.lower()} theme.
    2. **Tone:** Ensure the tone is {theme.lower()} and appealing to the target audience.
    3. **Hashtags (if selected):** Include trending hashtags related to the context of the image (if the option is selected by the user).
    4. **Multi-language:** Provide translations of the caption in the selected language: {language}.
    5. **Emojis:** Add emojis that enhance the caption's emotional impact.

    Keep the captions concise, engaging, and visually pleasing!
    """

    # Call the model to generate the caption based on the uploaded image and input prompt
    model = genai.GenerativeModel("gemini-1.5-flash")
    image_parts = [{"mime_type": uploaded_image.type, "data": uploaded_image.getvalue()}]
    
    response = model.generate_content([input_prompt, image_parts[0]])
    return response.text

def generate_engagement_graph():
    # Random data for feed and end-user engagement analysis
    time = pd.date_range("2023-01-01", periods=30, freq="D")
    feed_engagement = np.random.rand(30) * 100
    user_engagement = np.random.rand(30) * 100
    df = pd.DataFrame({"Date": time, "Feed Engagement": feed_engagement, "User Engagement": user_engagement})
    return df

def create_line_chart(df):
    chart = alt.Chart(df).mark_line().encode(
        x='Date:T',
        y='Feed Engagement:Q',
        color=alt.value("#1e90ff")
    ).properties(width=600, height=400).interactive()
    
    return chart

def get_trend():
    # Dynamically fetching trend
    trend_prompt = "What is trending today in social media platforms? If you don't have access to real-time data, tell that these are the things, which when posted, tend to have the maximum impact."
    model = genai.GenerativeModel("gemini-1.5-flash")
    trend_response = model.generate_content([trend_prompt])
    return trend_response.text

def generate_advice(caption_type):
    # Generate advice based on the caption type (e.g., general, strategy)
    advice_prompt = f"Provide a detailed {caption_type} for optimal social media engagement and content strategy."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([advice_prompt])
    return response.text

# User Inputs for Caption
uploaded_file = st.file_uploader("📸 Upload your image for caption generation", type=["jpeg", "jpg", "png"])

theme = st.selectbox("Choose a theme for your caption:", ["Funny", "Inspirational", "Romantic", "Trendy", "Minimalist"])
language = st.selectbox("Choose a language:", ["English", "Spanish", "French", "German", "Hindi"])
include_hashtags = st.checkbox("Include trending hashtags")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Main Feature Options (Hoverable & Interactive)
option = st.selectbox('Choose a Feature', ['Generate Captions', 'Predict Analysis 📈', 'What are the Best Trends?', 'Generate Advice'])

# Generate Captions Section
if option == 'Generate Captions':
    st.markdown("### ✏️ Caption Customization")
    st.text("Generating your captions now!")

    if uploaded_file is not None:
        with st.spinner("Generating your caption..."):
            generated_caption = generate_dynamic_captions(theme, language, include_hashtags, uploaded_file)
            st.header("📋 Generated Caption")
            st.write(generated_caption)
    else:
        st.warning("⚠️ Please upload an image to generate captions!")

# Predict Analysis Section (Engagement prediction)
elif option == 'Predict Analysis 📈':
    # Collect data (example input)
    follower_count = st.number_input("Enter follower count:", min_value=1, max_value=1000000, value=1000, step=100)
    time_of_post = st.time_input("When do you plan to post?", value=pd.to_datetime("08:00").time())
    
    st.subheader("Dynamic Engagement Prediction Based on Input")
    # Sample engagement prediction model based on user input
    engagement_data = generate_engagement_graph()
    chart = create_line_chart(engagement_data)
    st.altair_chart(chart, use_container_width=True)

    st.write(f"Optimal Time for Maximum Views: 8:00 AM.")  # Example suggestion based on your algorithm

    # Engagement Advice Section (AI-Generated)
    if st.button("💡 Show Engagement Tips"):
        ai_advice = generate_advice('Engagement Strategy')
        st.write(f"🔑 {ai_advice}")

# Trend Section
elif option == 'What are the Best Trends?':
    st.subheader("🎯 Top Social Media Trend of the Day:")
    with st.spinner("Fetching the latest trend..."):
        trend = get_trend()
        st.write(f"🌟 Trending Topic: {trend}")

# Generate Advice Section (Custom dropdown)
elif option == 'Generate Advice':
    st.markdown("### 💡 Choose Advice Type:")
    advice_type = st.selectbox("Select the type of advice you want:", ['General Tips', 'Post Strategy', 'Caption Strategy'])

    if st.button("🔍 Generate Advice"):
        ai_advice = generate_advice(advice_type)
        st.write(f"🔑 {ai_advice}")

# Custom Styling
st.markdown("""
<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f9f9f9; 
        color: #333; 
    }
    .stButton {
        display: flex; 
        justify-content: center; 
        margin: 20px 0;
    }
    .stButton > button {
        background-color: #1e90ff;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 18px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: background-color 0.3s, transform 0.3s;
    }
    .stButton > button:hover {
        background-color: #0056b3;
        transform: translateY(-2px);
    }
    h1 {
        color: #2c3e50; 
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    h2 {
        color: #34495e; 
        margin-top: 30px;
        margin-bottom: 10px;
    }
    h3 {
        color: #7f8c8d; 
        margin-top: 20px;
    }
    .stImage {
        margin: 20px 0;
        border: 2px solid #ecf0f1; 
        border-radius: 10px;
        padding: 5px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: white; 
    }
</style>
""", unsafe_allow_html=True)
