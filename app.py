import pytesseract
from PIL import Image
import gradio as gr
import re

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def perform_ocr(image):
    text = pytesseract.image_to_string(image, lang='hin+eng')
    return text

def search_first_keyword_in_text(text, keyword):
    if keyword:
        text = text.replace('\n', ' ')
        sentences = re.split(r'(?<=[.!?]) +', text)
        for sentence in sentences:
            if re.search(keyword, sentence, re.IGNORECASE):
                highlighted_sentence = re.sub(f'({re.escape(keyword)})', r'<b>\1</b>', sentence, flags=re.IGNORECASE)
                return highlighted_sentence.strip()
        return "No matching sentence found."
    else:
        return "Please enter a keyword to search."

def ocr_and_search(image, keyword):
    try:
        extracted_text = perform_ocr(image)
        search_result = search_first_keyword_in_text(extracted_text, keyword)
        return extracted_text, search_result
    except Exception as e:
        return str(e), str(e)

def web_app():
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

if __name__ == "__main__":
    web_app()