# import io
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfpage import PDFPage
# import docx2txt
# import re
# import spacy
# import pandas as pd
# from flask import Flask, request, jsonify

from flask import Flask, render_template, request
import PyPDF2
import docx2txt
import re
import spacy

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    with file_path.stream as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_names_from_text(text):
    doc = nlp(text)
    names = []

    for entity in doc.ents:
        if entity.label_ == 'PERSON':
            names.append(entity.text)

    return names[0]

def extract_contact_info(text):
    email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phone = re.findall(r'(\(?\d{3}\)?[-.\s]?)(\d{3}[-.\s]?)(\d{4})', text)
    if email and phone:
        return email[0], phone[0]
    elif email:
        return email[0], None
    elif phone:
        return None, phone[0]
    else:
        return None, None

# def extract_education(text):
#     education = re.findall(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}\s-\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}|(20\d{2})\s-\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}|(20\d{2})\s-\s(?:Present))\n([\w\s.]+),\s([\w\s]+)', text)
#     return education
def extract_education(text):
    education = re.findall(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}\s-\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}|(20\d{2})\s-\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}|(20\d{2})\s-\s(?:Present))\n([\w\s.]+),\s([\w\s]+)', text)
    return education

def extract_skills(text):
    skills = re.findall(r'[\n,]\s*([A-Za-z\s]+)\s*[,:-]', text)
    return skills

def extract_experience(text):
    experience = re.split(r'\n\d{4}\s-\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}', text)
    return [exp.strip() for exp in experience if exp.strip()]

def home():
    return render_template('application.html')


@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        resume = request.files['resume']
        if resume.filename.endswith('.pdf'):
            text = extract_text_from_pdf(resume)
        elif resume.filename.endswith('.docx'):
            text = extract_text_from_docx(resume)
        else:
            return 'Invalid file format. Please upload a PDF or DOCX file.'
            
        name = extract_names_from_text(text)
        email, phone = extract_contact_info(text)
        education = extract_education(text)
        skills = extract_skills(text)
        experience = extract_experience(text)
        return render_template('result.html', name=name, email=email, phone=phone, education=education, skills=skills, experience=experience)
    return render_template('application.html')   

if __name__ == '__main__':
    app.run(debug=True)

