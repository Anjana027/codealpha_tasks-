import gradio as gr
from deep_translator import GoogleTranslator
import pyttsx3
import pyperclip

# Initialize TTS engine
tts_engine = pyttsx3.init()

# Language code mapping (from language name to code)
LANGUAGES = {
    'english': 'en',
    'french': 'fr',
    'spanish': 'es',
    'german': 'de',
    'italian': 'it',
    'portuguese': 'pt',
    'russian': 'ru',
    'japanese': 'ja',
    'korean': 'ko',
    'chinese': 'zh',
    # Add more as needed
}

# Helper to get language code
def get_lang_code(lang_name):
    return LANGUAGES.get(lang_name.lower(), 'en')

# Core translation function
def translate_text(text, src_lang, dest_lang, read_aloud, copy_clipboard):
    src_code = get_lang_code(src_lang)
    dest_code = get_lang_code(dest_lang)
    try:
        translated = GoogleTranslator(source=src_code, target=dest_code).translate(text)
        if copy_clipboard:
            pyperclip.copy(translated)
        if read_aloud:
            tts_engine.say(translated)
            tts_engine.runAndWait()
        return translated
    except Exception as e:
        return f"Translation failed: {e}"

def clear_all():
    return "", ""

# Language list for dropdown
langs = list(LANGUAGES.keys())

with gr.Blocks(title="🌍 Language Translation Tool") as demo:
    gr.Markdown("# 🌍 Language Translation Tool")
    input_text = gr.Textbox(label="Enter text to translate:", lines=4, placeholder="Type here...")
    with gr.Row():
        src_dropdown = gr.Dropdown(choices=langs, value="english", label="Select source language")
        dest_dropdown = gr.Dropdown(choices=langs, value="french", label="Select target language")
    with gr.Row():
        read_aloud_checkbox = gr.Checkbox(label="🔊 Read Aloud", value=False)
        copy_checkbox = gr.Checkbox(label="📋 Copy Translated Text", value=False)
    with gr.Row():
        translate_btn = gr.Button("Translate")
        clear_btn = gr.Button("Clear")
    output_text = gr.Textbox(label="Translated Text", lines=4)
    translate_btn.click(
        fn=translate_text,
        inputs=[input_text, src_dropdown, dest_dropdown, read_aloud_checkbox, copy_checkbox],
        outputs=output_text
    )
    clear_btn.click(fn=clear_all, outputs=[input_text, output_text])

demo.launch()
