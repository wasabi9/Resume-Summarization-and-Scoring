# Resume-Summarization-and-Scoring
This is a CLI tool to summarise and rate technical resumes
The tool uses Named Entity Recognition pipeline of Spacy for Resume Summarization
Resume Rating is done using extraction of features from resumes(Skills, Exp. and so on) and it's similarity with Job Description for the role (Using Cosine Similarity)

## Project Pipeline

1. Dataset - 
    Training & Validation : DataTurks (https://www.kaggle.com/dataturks/resume-entities-for-ner)
    Testing : Kaggle Dataset (https://www.kaggle.com/palaksood97/resume-dataset)

2. Named Entity Recognition (identify entities in the resume,i.e Name, Skills, Experience and so on) - 
    It uses the the ner pipeline of spacy which is trained and validated using the annotated resume dataset

3. Hybrid Resume Ranking System - 
    Uses Degree, Designation, Experience, Skills and resume-JD similarity to prepare a ensemble score on a scale of 1-10
    - Degree, Designation, Expereince - Based on a rule-based pattern search algorithm
    - Skills and Resume-JD Similarity - Uses the Trained NER Model from previous step and Cosine Similarity algorithm
    Ensemble score is a weighted average of all these individual factors

## 