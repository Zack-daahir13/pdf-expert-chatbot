from PyPDF2 import PdfReader
from transformers import pipeline

summarizer = pipeline("summarization")

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def summarize_text(text):
    # Only summarize first 1000 words for performance
    short_text = text[:1000]
    summary = summarizer(short_text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']
def record_and_transcribe():
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I did not understand that."
    except sr.RequestError:
        return "Sorry, there was an error with the speech recognition service."
def speak_text(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()