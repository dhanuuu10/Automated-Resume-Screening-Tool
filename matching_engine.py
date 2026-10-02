

import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from resume_parser import extract_resume_text
from information_extractor import extract_candidate_information


# List of technical skills
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


# STEP 6: Read job description
def read_job_description(file_path):

    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError("Job description file not found.")

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Extract job title
def extract_job_title(text):

    pattern = r'Job Title\s*:\s*(.+)'
    result = re.search(pattern, text, re.IGNORECASE)

    if result:
        return result.group(1).strip()

    return "Not Found"


# Extract required skills
def extract_required_skills(text):

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


# Extract required education
def extract_required_education(text):

    lines = text.splitlines()

    for i, line in enumerate(lines):

        if line.strip().lower().startswith(
            ("education", "educational qualification")
        ):

            education = []

            for next_line in lines[i + 1:]:

                clean_line = next_line.strip()

                if not clean_line:
                    continue

                if clean_line.lower().startswith(
                    ("experience", "required skills",
                     "job responsibilities")
                ):
                    break

                education.append(clean_line)

            if education:
                return " ".join(education)

    return "Not Found"


# Extract required experience
def extract_required_experience(text):

    pattern = r'Experience\s*:\s*(.+)'
    result = re.search(pattern, text, re.IGNORECASE)

    if result:
        return result.group(1).strip()

    return "Not Specified"


# Process the complete job description
def process_job_description(file_path):

    text = read_job_description(file_path)

    job_details = {
        "Job Title": extract_job_title(text),
        "Required Skills": extract_required_skills(text),
        "Education": extract_required_education(text),
        "Experience": extract_required_experience(text)
    }

    return job_details


# STEP 7: Calculate text similarity using TF-IDF
def calculate_similarity(resume_text, job_description_text):

    if not resume_text.strip() or not job_description_text.strip():
        return 0.0

    documents = [resume_text, job_description_text]

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)


# Compare resume skills with required job skills
def compare_skills(resume_text, job_description_text):

    candidate_info = extract_candidate_information(resume_text)

    candidate_skills = candidate_info["Skills"]

    required_skills = extract_required_skills(job_description_text)

    matched_skills = [
        skill for skill in required_skills
        if skill in candidate_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in candidate_skills
    ]

    if required_skills:
        skill_match_percentage = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        skill_match_percentage = 0.0

    return {
        "Candidate Skills": candidate_skills,
        "Required Skills": required_skills,
        "Matched Skills": matched_skills,
        "Missing Skills": missing_skills,
        "Skill Match Percentage": round(skill_match_percentage, 2)
    }


# Main resume matching function
def match_resume_to_job(resume_text, job_description_text):

    similarity_score = calculate_similarity(
        resume_text,
        job_description_text
    )

    skill_results = compare_skills(
        resume_text,
        job_description_text
    )

    return {
        "Similarity Score": similarity_score,
        **skill_results
    }

# STEP 8: Rank multiple candidates
def rank_candidates(resume_folder, job_description_path):

    resume_folder = Path(resume_folder)

    # Read the job description
    job_text = read_job_description(job_description_path)

    candidate_results = []

    # Find all supported resume files
    resume_files = []

    for extension in ["*.pdf", "*.docx", "*.txt"]:
        resume_files.extend(resume_folder.glob(extension))

    if not resume_files:
        raise FileNotFoundError("No resumes found in the resume folder.")

    # Process each resume
    for resume_file in resume_files:

        try:

            # Extract resume text
            resume_text = extract_resume_text(resume_file)

            # Extract candidate details
            candidate_info = extract_candidate_information(resume_text)

            # Calculate matching results
            results = match_resume_to_job(resume_text, job_text)

            # Combine similarity and skill match scores
            final_score = (
                results["Similarity Score"] * 0.5
                + results["Skill Match Percentage"] * 0.5
            )

            # Store candidate results
            candidate_results.append({

                "Name": candidate_info["Name"],
                "Email": candidate_info["Email"],
                "Resume": resume_file.name,
                "Similarity Score": results["Similarity Score"],
                "Skill Match Percentage": results["Skill Match Percentage"],
                "Final Score": round(final_score, 2),
                "Matched Skills": ", ".join(results["Matched Skills"]),
                "Missing Skills": ", ".join(results["Missing Skills"])

            })

        except Exception as error:

            print(f"Could not process {resume_file.name}: {error}")

    # Sort candidates by final score
    candidate_results.sort(
        key=lambda candidate: candidate["Final Score"],
        reverse=True
    )

    # Assign ranks
    for index, candidate in enumerate(candidate_results, start=1):

        candidate["Rank"] = index

    return candidate_results


# Main program execution
if __name__ == "__main__":

    resume_folder = "data/resumes"

    job_path = "data/job_descriptions/python_developer.txt"

    try:

        ranked_candidates = rank_candidates(
            resume_folder,
            job_path
        )

        print("\nCANDIDATE RANKING RESULTS")
        print("=========================")

        for candidate in ranked_candidates:

            print("\nRank:", candidate["Rank"])
            print("Name:", candidate["Name"])
            print("Email:", candidate["Email"])
            print("Resume:", candidate["Resume"])
            print("Similarity Score:", candidate["Similarity Score"], "%")
            print("Skill Match:", candidate["Skill Match Percentage"], "%")
            print("Final Score:", candidate["Final Score"], "%")
            print("Matched Skills:", candidate["Matched Skills"])
            print("Missing Skills:", candidate["Missing Skills"])

    except Exception as error:

        print("Error:", error)
