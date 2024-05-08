import textract
import re
import spacy
import openpyxl
from parser4 import start, is_header, classify_header_type
import os
import pdfplumber

nlp = spacy.load("en_core_web_sm")

ambiguous=["PROFESSIONAL DEVELOPMENT WORKSHOPS","Publication", "Editorial Activities" ]

publication_headers = [
    "Publications", "Journal Articles", "Articles", "Published Works",
    "Working Papers", "Published Abstracts",
    "Published Research", "Research Papers", "Scientific Publications", 
    "Research Projects",  "White Papers", "Discussion Papers", "Review Articles",
    "Published Letters","Manuscript","Peer reviewed journals ","Refereed Journals",
    "Refereed Proceedings", "paper proceedings"
]

book_headers= ["Books and Book Chapters", "Books", "Book chapters","Book reviews"]

conference_headers=["Conference Proceedings","Conference presentations", "Conference Workshops","Presentations", "Conference papers","PEER REVIEWED PROCEEDINGS"]
def remove_text_in_parentheses(line):
    """
    Removes text within parentheses, including the parentheses themselves.
    """
    # Regular expression to match content within parentheses
    new_line = re.sub(r'\(.*?\)', '', line)
    return new_line.strip()

def is_all_caps_header(line):
    """
    Checks if a given line is a header and if it's written in all capital letters.
    Returns True if the line is a header in all caps, False otherwise.
    """
    cleaned_line = remove_text_in_parentheses(line)
    return cleaned_line.isupper()

def check_headers_capital(file_path):
    text = textract.process(file_path).decode('utf-8')
    lines = text.split('\n')
    headers_capital = True
    header_types = ["Publication", "Conference", "Book Chapter"]

    for line in lines:
        line = line.strip()
        if line and is_header(line):
            # Determine the type of the header
            header_type = classify_header_type(line)
            if header_type and header_type in header_types:
                print(line)
                if not is_all_caps_header(line):
                    headers_capital = False
                    break
                else :
                    headers_capital=True
                    break
    return headers_capital

def parse_resume(file_path,year):
    if is_pdf(file_path):
        parse_pdf(file_path)
    else:
        if check_headers_capital(file_path):
            combined_data=start(file_path, True,year)
        else:
            combined_data=start(file_path, False,year)
    return combined_data

def is_pdf(file_path):
    return file_path.lower().endswith('.pdf')

def parse_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        all_text = ''
        for page in pdf.pages:
            all_text += page.extract_text() + '\n'
    return all_text

# def parse_resumes(directory_path):
#     # Loop over all files in the directory
#     for filename in os.listdir(directory_path):
#         # Construct the full file path
#         file_path = os.path.join(directory_path, filename)
        
#         # Check if the current file is a .docx file
#         if file_path.endswith('.docx'):
#             # Print the file path
#             print(f"Processing: {file_path}")
#             # Print the output of check_headers_capital for the file
#             headers_capital = check_headers_capital(file_path)
#             print(f"Headers in all caps: {headers_capital}")
#         else:
#             print(f"Skipping non-docx file: {file_path}")

# Directory containing all resumes
# directory_path = r"C:\Users\Parth\Downloads\General\General\all_resumes"
# parse_resumes(directory_path)

# file_path = r"C:\Users\Parth\Downloads\General\General\all_resumes\Devers  CV- December  2023 (1).docx"
# parse_resume(file_path)