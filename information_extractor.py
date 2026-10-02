
import re

from resume_parser import extract_resume_text


# List of technical skills to identify
SKILLS_LIST = [
    "Python", "Java", "C++", "C", "SQL",
    "HTML", "CSS", "JavaScript",
    "Django", "Flask", "React",
    "Machine Learning", "Deep Learning",
    "Data Analysis", "Pandas", "NumPy",
    "Scikit-learn", "TensorFlow",
    "Power BI", "Excel",
    "AWS", "Azure", "Git", "GitHub",
    "MongoDB", "MySQL", "PostgreSQL",
    "Communication", "Problem Solving"
]


# Function to extract email address
def extract_email(text):

    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    result = re.search(pattern, text)

    if result:
        return result.group()

    return "Not Found"


# Function to extract phone number
def extract_phone(text):

    pattern = r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)'

    result = re.search(pattern, text)

    if result:
        return result.group()

    return "Not Found"


# Function to extract candidate name
def extract_name(text):

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        result = re.match(
            r'^(?:Name|Candidate Name)\s*[:\-]\s*(.+)$',
            line,
            re.IGNORECASE
        )

        if result:
            return result.group(1).strip()

    # Fallback: use the first non-empty line
    for line in lines:

        line = line.strip()

        if line and not re.search(r'@|https?://|www\.', line):
            return line

    return "Not Found"


# Function to extract technical skills
def extract_skills(text):

    found_skills = []

    for skill in SKILLS_LIST:

        pattern = (
            r'(?<![a-zA-Z0-9])'
            + re.escape(skill)
            + r'(?![a-zA-Z0-9])'
        )

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


# Function to extract education and experience sections
def extract_section(text, section_name):

    lines = text.splitlines()

    section_started = False
    section_content = []

    headings = [
        "education",
        "academic qualifications",
        "qualification",
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "technical skills",
        "skills",
        "projects",
        "certifications",
        "career objective",
        "summary"
    ]

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        heading = clean_line.rstrip(":").strip().lower()

        if not section_started:

            if heading in [
                section_name,
                "academic qualifications",
                "qualification"
            ] and section_name == "education":

                section_started = True
                continue

            if heading in [
                "experience",
                "work experience",
                "professional experience",
                "employment history"
            ] and section_name == "experience":

                section_started = True
                continue

        else:

            if heading in headings:
                break

            section_content.append(clean_line)

    if section_content:
        return "\n".join(section_content)

    return "Not Found"


# Main function to extract all candidate information
def extract_candidate_information(text):

    candidate = {

        "Name": extract_name(text),

        "Email": extract_email(text),

        "Phone": extract_phone(text),

        "Skills": extract_skills(text),

        "Education": extract_section(text, "education"),

        "Experience": extract_section(text, "experience")
    }

    return candidate


# Main program execution
if __name__ == "__main__":

    resume_path = input("Enter resume file path: ")

    try:

        # Read resume using Step 4 function
        resume_text = extract_resume_text(resume_path)

        # Extract candidate information
        candidate_info = extract_candidate_information(resume_text)

        print("\nCANDIDATE INFORMATION")
        print("----------------------")

        for key, value in candidate_info.items():

            print(f"\n{key}:")
            print(value)

    except Exception as error:

        print("Error:", error)
