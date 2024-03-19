import streamlit as st
from PIL import Image
import pytesseract
import openai

# Streamlit page configuration
st.set_page_config(page_title="Tickets con AI", layout="wide")

def extract_text(image):
    """Extracts text from an image using pytesseract."""
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error in text extraction: {str(e)}"

def parse_receipt_with_gpt(text):
    """Sends extracted text to GPT for parsing."""
    try:
        openai.api_key = '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'
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Parse the following receipt details and respond only with a JSON format that includes Nombre del Comercio, Negocio Number, Fecha, Hora, Metodo de Pago, Last digits of the card, and the Total: {text}"}

            ]
        )
        if response.choices:
            # Assuming the latest response format in GPT-4 API
            latest_message = response.choices[0].message.content
            return latest_message
        else:
            return "No response"
    except Exception as e:
        return f"API Call Error: {str(e)}"

# Streamlit UI
st.title("Tickets con IA")
st.write("Sube o toma una foto de tu ticket.")

tab1,tab2 = st.tabs(["Subir Foto", "Tomar Foto"])

with tab1:
    # File uploader allows user to add their own image
    uploaded_file = st.file_uploader("Selecciona tu archivo", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
       image = Image.open(uploaded_file)
       st.image(image, caption="Ticket subido", use_column_width=True)
       if st.button("Analizar con IA"):
          with st.spinner('Extrayendo información y analizando...'):
            extracted_text = extract_text(image)
            parsed_text = parse_receipt_with_gpt(extracted_text)
            st.write("Texto obtenido:")
            st.json(parsed_text)

with tab2:
    uploaded_file = st.camera_input("Toma una foto")
    if uploaded_file is not None:
       image = Image.open(uploaded_file)
       st.image(image, caption="Ticket subido", use_column_width=True)
       if st.button("Analizar con IA"):
          with st.spinner('Extrayendo información y analizando...'):
            extracted_text = extract_text(image)
            parsed_text = parse_receipt_with_gpt(extracted_text)
            st.write("Texto obtenido:")
            st.json(parsed_text)



