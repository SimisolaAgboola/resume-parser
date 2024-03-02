from flask import Flask, render_template, request
import os
import re
import boto3
from botocore.exceptions import NoCredentialsError
import csv
import requests
from bs4 import BeautifulSoup

# Initialize Textract client
textract_client = boto3.client('textract',region_name='us-east-2',aws_access_key_id='AKIAVRUVRFJ2NDVZQBCA',aws_secret_access_key='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')

app = Flask(__name__)

def extract_text_from_pdf(file):
    
    #read file directly
    file_bytes = bytearray(file.read())

    # Call Amazon Textract to detect text in the doccument
    response = textract_client.detect_document_text(Document={'Bytes': file_bytes})

    # Extract text lines from the response
    if 'Blocks' in response and response['Blocks']:
        lines = [line['Text'] for line in response['Blocks'] if line['BlockType'] == 'LINE']

        # Join lines into a single string
        text = ' '.join(lines)
    else:
        text = "No text detected in the document."
    return text

def extract_university(text):
    universities = []
    with open('world-universities.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:  # Check if row has at least two columns
                universities.append(row[1].lower())
    university = []
    listex = universities
    listsearch = [text.lower()]
    for i in range(len(listex)):
        for ii in range(len(listsearch)):
            if re.findall(listex[i], re.sub(' +', ' ', listsearch[ii])):
                university.append(listex[i])

    return "".join(university)

def extract_degree(text):
    degree = []
    pattern = r"\b(?=[A-Z])((?:AB|ABA|AA|AS|AAS|(?:B(?:achelors?)?\.?(?:\s(?:of))?\.?(?:\s(?:Science|Arts|Business|Education|Liberal\sArts|Social\sWork|Fine\sArts)))|(?:M(?:asters?)?|Ph\.D)\.?\.?(?:\s(?:of))?\.?(?:\s(?:Science|Arts|Business Administration|Education|Engineering|International Business|Fine Arts|Humanities|Arts\sin\sTeaching))))\b"
    matches = re.findall(pattern, text)
    for match in matches:
        degree.append(match.strip())
    return "".join(degree)

def extract_major(text):
    # Find degrees in the text
    degrees = extract_degree(text)
    
    college_majors = []
    with open('college_majors.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            college_majors.append(row)
    major = ''
    for degree in degrees:
        # Find the position of the degree in the text
        start_pos = text.lower().find(degree.lower())
        if start_pos != -1:
            # Search for majors only after the degree
            text_after_degree = text[start_pos + len(degree):]
            for major_row in college_majors:
                major_name = major_row[0]  # Extract the major name from the row
                if major_name.lower() in text_after_degree.lower():
                    major += major_name + ', '  # Append the major to the major variable
                    break
        if major:
            break
    return major.strip(', ')

def extract_skills(text):
    skills = ""
    skills_list = []
    # Open the .txt file and read skills into skills_list
    with open('LINKEDIN_SKILLS_ORIGINAL.txt', 'r') as file:
        for line in file:
            skills_list.append(line.strip())

    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills += skill+ ", "      
    return skills

def extract_information(text):
    lines = text.split(' ') 

    #regular expressions for email and phone
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{3}\b')
    phone_pattern = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')

    # Extract information using regular expressions
    email_match = email_pattern.search(text)
    phone_match = phone_pattern.search(text)

    # Get extracted information or return empty array if not found
    name = lines[0] + ' ' + lines[1] if lines else ""
    email = email_match.group() if email_match else []
    phone = phone_match.group() if phone_match else []
    university = extract_university(text)
    degree = extract_degree(text)
    major = extract_major(text)
    skills = extract_skills(text)

    return name, email, phone, university, skills, degree, major

def home():
    return render_template('application.html')

@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        resume = request.files['resume']
        text = extract_text_from_pdf(resume)
        name, email, phone, university, skills, degree, major = extract_information(text)
        return render_template('result.html', name=name, email=email, phone=phone, university=university, skills=skills, degree=degree, major=major)
    return render_template('application.html')   

if __name__ == '__main__':
    app.run(debug=True)

