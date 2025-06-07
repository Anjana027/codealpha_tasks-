from dash import Dash, dcc, html, Input, Output, State
from deep_translator import GoogleTranslator
import pyttsx3
import pyperclip

app = Dash(__name__)

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
    'chinese': 'zh'
}

def get_lang_code(lang_name):
    return LANGUAGES.get(lang_name.lower(), 'en')

app.layout = html.Div([
    html.H1("🌍 Language Translation Tool"),
    dcc.Textarea(id="input-text", placeholder="Type here...", style={"width": "100%", "height": 100}),
    html.Div([
        dcc.Dropdown(list(LANGUAGES.keys()), "english", id="src-lang"),
        dcc.Dropdown(list(LANGUAGES.keys()), "french", id="dest-lang"),
    ], style={"display": "flex"}),
    html.Div([
        dcc.Checklist(["🔊 Read Aloud"], [], id="read-aloud"),
        dcc.Checklist(["📋 Copy Translated Text"], [], id="copy-clipboard"),
    ], style={"display": "flex"}),
    html.Button("Translate", id="translate-btn", n_clicks=0),
    dcc.Textarea(id="output-text", style={"width": "100%", "height": 100, "readOnly": True}),
])

@app.callback(
    Output("output-text", "value"),
    Input("translate-btn", "n_clicks"),
    State("input-text", "value"),
    State("src-lang", "value"),
    State("dest-lang", "value"),
    State("read-aloud", "value"),
    State("copy-clipboard", "value"),
)
def translate(n_clicks, input_text, src_lang, dest_lang, read_aloud, copy_clipboard):
    if not input_text:
        return ""
    src_code = get_lang_code(src_lang)
    dest_code = get_lang_code(dest_lang)
    try:
        translated = GoogleTranslator(source=src_code, target=dest_code).translate(input_text)
        if read_aloud:
            engine = pyttsx3.init()
            engine.say(translated)
            engine.runAndWait()
        if copy_clipboard:
            pyperclip.copy(translated)
        return translated
    except Exception as e:
        return f"Translation failed: {e}"

if __name__ == "__main__":
    app.run(debug=True)
