import google.generativeai as genai
import os

# Set up Gemini API key
GOOGLE_API_KEY = "AIzaSyAKL2JLf5USXrGvIz6QTA72soKdIuFg4y0"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

def get_fertilizer_strategy(fertilizer_name):
    """
    Fetches strategies for using a given fertilizer using Gemini AI.
    """
    prompt = f"Provide a short and concise best strategies and guidelines for using {fertilizer_name} fertilizer efficiently in farming. Make sure the response is organised"
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            return "No strategy found. Please try again."
    
    except Exception as e:
        return f"Error fetching strategy: {str(e)}"
