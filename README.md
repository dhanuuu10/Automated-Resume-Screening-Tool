
# Automated Resume Screening Tool

## Project Overview

The Automated Resume Screening Tool is a Python-based application that helps recruiters screen and rank multiple resumes according to a given job description.

The application extracts candidate information, identifies technical skills, calculates resume similarity, compares required skills, and ranks candidates based on their matching scores.

It provides an interactive dashboard using Streamlit.

## Objectives

- Automate the initial resume screening process.
- Extract candidate information from resumes.
- Identify technical skills and educational qualifications.
- Compare resumes with job descriptions.
- Calculate resume similarity and skill matching scores.
- Rank candidates according to their final matching scores.
- Generate downloadable screening reports.

## Features

- Supports PDF, DOCX and TXT resume formats.
- Extracts candidate name, email and phone number.
- Identifies technical skills, education and experience.
- Uses TF-IDF and cosine similarity for text comparison.
- Identifies matched and missing skills.
- Calculates candidate matching scores.
- Ranks multiple candidates.
- Displays interactive charts and progress bars.
- Allows CSV report downloads.

## Technologies Used

- Python 3.12
- Streamlit
- Pandas
- Scikit-learn
- PyPDF2
- python-docx
- Regular Expressions (Regex)
- TF-IDF
- Cosine Similarity

## Project Structure

Automated-Resume-Screening-Tool/

    data/
        resumes/
        job_descriptions/

    resume_parser.py
    information_extractor.py
    matching_engine.py
    app.py
    README.md

## Installation

### Step 1: Clone the repository

    git clone YOUR_GITHUB_REPOSITORY_URL

### Step 2: Open the project folder

    cd Automated-Resume-Screening-Tool

### Step 3: Create a virtual environment

    python -m venv venv

### Step 4: Activate the virtual environment

Windows:

    venv\Scripts\activate

### Step 5: Install required libraries

    pip install streamlit pandas scikit-learn PyPDF2 python-docx

## How to Run

Run the following command in the terminal:

    streamlit run app.py

The application will open in your web browser.

## Working Methodology

1. Upload multiple candidate resumes.
2. Enter the job description.
3. Extract text from uploaded resumes.
4. Extract candidate information and technical skills.
5. Process the job description.
6. Calculate similarity using TF-IDF and cosine similarity.
7. Compare candidate skills with required skills.
8. Calculate the final matching score.
9. Rank candidates.
10. Display results and download the CSV report.

## Matching Score Formula

Final Score = (0.5 × Similarity Score) + (0.5 × Skill Match Percentage)

Both scores are expressed as percentages.

## Output

The application displays:

- Candidate ranking
- Candidate information
- Similarity score
- Skill matching percentage
- Final matching score
- Matched skills
- Missing skills
- Candidate comparison charts
- Downloadable CSV report

## Future Enhancements

- Add machine learning-based resume classification.
- Support additional resume formats.
- Improve candidate experience and education extraction.
- Add advanced skill matching using NLP.
- Add secure user authentication.
- Store candidate records in a database.

## Disclaimer

This project is an educational prototype. Its scores are intended to support initial resume screening and should not be used as the sole basis for hiring decisions. Human review is necessary.

## Author

Computer Engineering Student

## License

This project is developed for educational and learning purposes.
