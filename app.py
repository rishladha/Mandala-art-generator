import streamlit as st
import openai
import os
import base64
from PIL import Image
from io import BytesIO
import requests

def generate_mandala(api_key, prompt, color_palette):
    """Generate mandala art using DALL-E 3"""
    
    # Set OpenAI API key dynamically
    openai.api_key = api_key
    
    # Craft a detailed prompt based on user input and color palette
    if color_palette == "Black and White":
        detailed_prompt = f"Create a detailed, symmetrical mandala art in black and white inspired by the concept: '{prompt}'. The mandala should have intricate patterns, precise geometric shapes, and perfect radial symmetry."
    
    elif color_palette == "VIBGYOR":
        detailed_prompt = f"Create a detailed, symmetrical mandala art using the colors of the rainbow (violet, indigo, blue, green, yellow, orange, red) inspired by the concept: '{prompt}'. The mandala should have intricate patterns, precise geometric shapes, and perfect radial symmetry."
    
    elif color_palette == "Multicolor":
        detailed_prompt = f"Create a detailed, symmetrical mandala art in vibrant, diverse colors inspired by the concept: '{prompt}'. The mandala should have intricate patterns, precise geometric shapes, and perfect radial symmetry."
    
    elif "Gradient:" in color_palette:
        color = color_palette.split(":")[1].strip()
        detailed_prompt = f"Create a detailed, symmetrical mandala art using gradient shades of {color} inspired by the concept: '{prompt}'. The mandala should have intricate patterns, precise geometric shapes, and perfect radial symmetry."
    
    else:  # Single color
        detailed_prompt = f"Create a detailed, symmetrical mandala art in {color_palette} color inspired by the concept: '{prompt}'. The mandala should have intricate patterns, precise geometric shapes, and perfect radial symmetry."
    
    try:
        # Call DALL-E 3 API
        response = openai.images.generate(
            model="dall-e-3",
            prompt=detailed_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Get image URL
        image_url = response.data[0].url
        
        # Download the image
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        
        return image
    
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def get_image_download_link(img, filename="mandala.png", text="Download Mandala"):
    """Generate a download link for the image"""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">👉 {text}</a>'
    return href

def main():
    st.title("Mandala Art Generator")
    st.write("Create beautiful mandala art based on your inspiration")
    
    # Add API key input with password protection
    api_key = st.text_input("Enter your OpenAI API Key (starts with 'sk-'):", type="password")
    
    # Add a small help text
    st.caption("Your API key is not stored and is only used for this session")
    
    # User input for inspiration
    inspiration = st.text_input("Enter a word or phrase for inspiration:", "peace and harmony")
    
    # Color palette selection
    color_options = [
        "Black and White", 
        "VIBGYOR", 
        "Multicolor",
        "Red",
        "Blue",
        "Green",
        "Purple",
        "Pink",
        "Gold",
        "Silver",
        "Gradient: Blue",
        "Gradient: Purple",
        "Gradient: Sunset",
        "Gradient: Earth tones"
    ]
    
    color_palette = st.selectbox("Choose a color palette:", color_options)
    
    # Generate button - only enabled if API key is provided
    if st.button("Generate Mandala", disabled=not api_key):
        if not api_key:
            st.warning("Please enter your OpenAI API key to continue")
        else:
            with st.spinner("Creating your mandala... This may take a minute."):
                mandala_image = generate_mandala(api_key, inspiration, color_palette)
                
                if mandala_image:
                    st.image(mandala_image, caption=f"Mandala inspired by: {inspiration}", use_column_width=True)
                    
                    # Provide download link
                    st.markdown(get_image_download_link(mandala_image), unsafe_allow_html=True)
                    
                    # Save information
                    st.success("Your mandala has been created successfully!")

# Optional - add session state to remember API key during the session
if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

if __name__ == "__main__":
    main()
