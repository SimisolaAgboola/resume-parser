# Resume Parser  

This project is a Flask-based web application that parses resumes, extracts key information such as the applicant's name, email, phone number, university, degree, major, experience and skills, and displays the results on a web page. The application utilizes AWS Textract for text extraction from uploaded PDF documents and a custom trained spacy NER for classifying the information on the resume.  


## Features  

* Upload PDF resumes for parsing.
* Extracts basic information (name, email, phone number).
* Identifies university, degree, major, experience and skills from the resume.
* Utilizes AWS Textract for accurate text extraction from PDFs.
* Displays parsed results in a user-friendly format.
  

## Technology Stack
* __Flask__: Web framework for Python.
* __AWS Textract__: Service to extract text from documents.
* __Regular Expressions__: For pattern matching and data extraction.
* __Custom trained Spacy NER__: for pattern matching and data extraction
* __Kaggle dataset__: for training the spacy NER
* __HTML/CSS__: For the front-end user interface.
  

## Setup Instructions  

### Clone the Repository  

* git clone https://github.com/SimisolaAgboola/resume-parser.git
* cd resume-parser  

### Install Dependencies  

Create a virtual environment and install the required Python packages:  

* python3 -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt  

### AWS Setup  

Ensure you have an AWS account and set up AWS Textract. Store your credentials in a .env file in the project root:  

* AWS_ACCESS_KEY_ID=your-access-key-id
* AWS_SECRET_ACCESS_KEY=your-secret-access-key  

### Run the Application  

Start the Flask development server:  

* flask run
* Visit http://127.0.0.1:5000/ in your browser.  


## Future Improvements  

* Improve the nlp logic that extracts relevant data from the resume to increase parsing accuracy
* Improve UI/UX for a more seamless user experience.  

