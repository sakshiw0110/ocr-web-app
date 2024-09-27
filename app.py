import pytesseract
from PIL import Image
import gradio as gr
import re

# Path to the Tesseract-OCR installation
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Function to perform OCR on the image
def perform_ocr(image):
    # Extract text in both Hindi and English
    text = pytesseract.image_to_string(image, lang='hin+eng')
    return text

# Function to search for the first sentence containing the keyword
def search_first_keyword_in_text(text, keyword):
    if keyword:
        # Replace newlines with spaces to handle multi-line text properly
        text = text.replace('\n', ' ')
        
        # Split the text into sentences using both Hindi (।) and English punctuation (.!?)
        sentences = re.split(r'(?<=[.!?।])\s+', text)
        
        # Loop through sentences and search for the keyword
        for sentence in sentences:
            if re.search(keyword, sentence, re.IGNORECASE):
                # Highlight the keyword in the sentence
                highlighted_sentence = re.sub(f'({re.escape(keyword)})', r'<b>\1</b>', sentence, flags=re.IGNORECASE)
                return highlighted_sentence.strip()
        
        # Return if no matching sentence is found
        return "No matching sentence found."
    else:
        return "Please enter a keyword to search."

# Function to perform both OCR and keyword search
def ocr_and_search(image, keyword):
    try:
        # Perform OCR and search for the keyword in the extracted text
        extracted_text = perform_ocr(image)
        search_result = search_first_keyword_in_text(extracted_text, keyword)
        return extracted_text, search_result
    except Exception as e:
        return str(e), str(e)

# Function to launch the Gradio web app
def web_app():
    # Gradio interface for the web app
    interface = gr.Interface(
        fn=ocr_and_search,
        inputs=[
            gr.Image(type="pil", label="Upload Image"),
            gr.Textbox(placeholder="Enter keyword to search", label="Keyword Search")
        ],
        outputs=[
            gr.Textbox(label="Extracted Text", lines=10),
            gr.HTML(label="Search Result (First Matching Sentence)")
        ],
        title="OCR and Keyword Search Application"
    )
    interface.launch()

# Main function to launch the web app
if __name__ == "__main__":
    web_app()
