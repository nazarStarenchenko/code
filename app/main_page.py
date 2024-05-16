import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
import base64

def detect_ships(image):
    return np.array(image.convert('L'))

def get_image_download_link(img, text):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/jpg;base64,{img_str}" download="{text}.jpg">Download {text}</a>'
    return href

def main():
    st.text("Анна Машир, Ніколай Шевченко, Данило Шморгун, Назар Старенченко, Микола Романов\nКМ-31 мн/мп")
    
    # Upload image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display original image
        st.header("Original and Modified Images")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            original_image = Image.open(uploaded_file)
            st.image(original_image, caption="Original Image", use_column_width=True)
        
        # Button to convert image to grayscale
        if st.button("Detect ships"):
            with col2:
                st.subheader("Detected ships")
                grayscale_image = detect_ships(original_image)
                st.image(grayscale_image, caption="Detected ships", use_column_width=True)
                
    if st.button("Logout"):
        if 'logged_in' in st.session_state:
            st.session_state['logged_in'] = False  # Update the session state to not logged in
        st.experimental_rerun()  # Rerun the app to reflect the change