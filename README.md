Resume Parser
This project is a Flask-based web application that parses resumes, extracts key information such as the applicant's name, email, phone number, university, degree, major, and skills, and displays the results on a web page. The application utilizes AWS Textract for text extraction from uploaded PDF documents.

Features
Upload PDF resumes for parsing.
Extracts basic information (name, email, phone number).
Identifies university, degree, major, and skills from the resume.
Utilizes AWS Textract for accurate text extraction from PDFs.
Displays parsed results in a user-friendly format.

Technology Stack
Flask: Web framework for Python.
AWS Textract: Service to extract text from documents.
CSV and Regular Expressions: For pattern matching and data extraction.
NLP tokenizer: for pattern matching and data extraction
HTML/CSS: For the front-end user interface.


Setup Instructions
Clone the Repository
git clone https://github.com/your-username/resume-parser.git
cd resume-parser
Install Dependencies
Create a virtual environment and install the required Python packages:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
AWS Setup
Ensure you have an AWS account and set up AWS Textract. Store your credentials in a .env file in the project root:
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
Run the Application
Start the Flask development server:
flask run
Visit http://127.0.0.1:5000/ in your browser.

Usage
Upload a PDF resume via the provided form on the homepage.
The app will process the document using AWS Textract and display the extracted information such as:
Name
Email
Phone
University
Degree
Major
Skills

File Structure
resume-parser/
│
├── app.py                     # Main application logic
├── templates/
│   ├── application.html        # Home page template
│   └── result.html             # Result page template
├── static/
│   └── style.css               # CSS file for styling
├── world-universities.csv      # CSV file of universities for lookup
├── college_majors.csv          # CSV file of majors for lookup
├── LINKEDIN_SKILLS_ORIGINAL.txt # Text file containing common skills
├── .env                        # AWS credentials (not included in repo)
└── requirements.txt            # List of required Python packages

Future Improvements
Improve the nlp logic that extracts relevant data from the resume
Improve UI/UX for a more seamless user experience.
