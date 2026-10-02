
import streamlit as st
import pandas as pd
import tempfile
from pathlib import Path
from matching_engine import rank_candidates

# Page configuration
st.set_page_config(
    page_title="Automated Resume Screening Tool",
    page_icon="📄",
    layout="wide"
)

# Application title
st.title("📄 Automated Resume Screening Tool")
st.write(
    "Upload candidate resumes and compare them with a job description "
    "to identify the most suitable candidates."
)

st.divider()

# Upload resumes
st.subheader("1. Upload Candidate Resumes")

uploaded_resumes = st.file_uploader(
    "Upload PDF, DOCX or TXT resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# Enter job description
st.subheader("2. Enter Job Description")

job_description = st.text_area(
    "Paste the job description here:",
    height=250,
    placeholder="Enter job title, required skills, education and experience..."
)

# Analyze button
if st.button("Analyze Resumes", type="primary"):

    if not uploaded_resumes:
        st.error("Please upload at least one resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        try:
            with tempfile.TemporaryDirectory() as temp_folder:

                temp_path = Path(temp_folder)

                resume_folder = temp_path / "resumes"
                resume_folder.mkdir()

                # Save uploaded resumes temporarily
                for index, uploaded_file in enumerate(
                    uploaded_resumes, start=1
                ):

                    original_name = Path(uploaded_file.name).name
                    saved_name = f"{index}_{original_name}"

                    file_path = resume_folder / saved_name

                    file_path.write_bytes(
                        uploaded_file.getbuffer()
                    )

                # Save job description temporarily
                job_path = temp_path / "job_description.txt"

                job_path.write_text(
                    job_description,
                    encoding="utf-8"
                )

                # Process resumes
                with st.spinner("Analyzing resumes..."):

                    results = rank_candidates(
                        resume_folder,
                        job_path
                    )

                if not results:

                    st.warning(
                        "No resumes could be processed. "
                        "Please check the uploaded files."
                    )

                else:

                    st.success("Resume analysis completed!")

                    df = pd.DataFrame(results)

                    # Screening summary
                    st.subheader("3. Screening Summary")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Total Candidates",
                        len(df)
                    )

                    col2.metric(
                        "Highest Matching Score",
                        f"{df['Final Score'].max()}%"
                    )

                    col3.metric(
                        "Average Matching Score",
                        f"{df['Final Score'].mean():.2f}%"
                    )

                    # Candidate ranking table
                    st.subheader("4. Candidate Ranking")

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Candidate performance chart
                    st.subheader("5. Candidate Performance Comparison")

                    chart_df = df.set_index("Name")[
                        [
                            "Final Score",
                            "Similarity Score",
                            "Skill Match Percentage"
                        ]
                    ]

                    st.bar_chart(chart_df)

                    # Skill matching chart
                    st.subheader("6. Skill Matching Comparison")

                    skill_chart = df.set_index("Name")[
                        ["Skill Match Percentage"]
                    ]

                    st.bar_chart(skill_chart)

                    # Individual candidate details
                    st.subheader("7. Candidate Details")

                    for _, candidate in df.iterrows():

                        with st.expander(
                            f"Rank {candidate['Rank']} - {candidate['Name']}"
                        ):

                            st.write(
                                "**Email:**",
                                candidate["Email"]
                            )

                            st.write(
                                "**Resume:**",
                                candidate["Resume"]
                            )

                            st.write(
                                "**Similarity Score:**",
                                f"{candidate['Similarity Score']}%"
                            )

                            st.write(
                                "**Skill Match:**",
                                f"{candidate['Skill Match Percentage']}%"
                            )

                            st.write(
                                "**Final Score:**",
                                f"{candidate['Final Score']}%"
                            )

                            # Progress bar
                            final_score = max(
                                0,
                                min(100, int(candidate["Final Score"]))
                            )

                            st.progress(final_score)

                            st.write(
                                "**Matched Skills:**",
                                candidate["Matched Skills"] or "None"
                            )

                            st.write(
                                "**Missing Skills:**",
                                candidate["Missing Skills"] or "None"
                            )

                    # Download report
                    st.subheader("8. Download Screening Report")

                    csv_data = df.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(
                        label="Download Results as CSV",
                        data=csv_data,
                        file_name="candidate_screening_results.csv",
                        mime="text/csv"
                    )

        except Exception as error:

            st.error(f"An error occurred: {error}")

st.divider()

st.caption(
    "Privacy Notice: Uploaded resumes are stored temporarily during "
    "analysis and are not intentionally saved by this app. "
    "This prototype provides decision-support scores only. "
    "Human review is required for hiring decisions."
)
