# Resume-Summarization-and-Scoring
This is a CLI tool to summarise and rate technical resumes
The tool uses Named Entity Recognition pipeline of Spacy for Resume Summarization
Resume Rating is done using extraction of features from resumes(Skills, Exp. and so on) and it's similarity with Job Description for the role (Using Cosine Similarity)

## Project Pipeline

1. Dataset - 
    - Training & Validation : DataTurks (https://www.kaggle.com/dataturks/resume-entities-for-ner)
    - Testing : Kaggle Dataset (https://www.kaggle.com/palaksood97/resume-dataset)

2. Named Entity Recognition (identify entities in the resume,i.e Name, Skills, Experience and so on) - 
    It uses the the ner pipeline of spacy which is trained and validated using the annotated resume dataset

3. Hybrid Resume Ranking System - 
    Uses Degree, Designation, Experience, Skills and resume-JD similarity to prepare a ensemble score on a scale of 1-10
    - Degree, Designation, Expereince - Based on a rule-based pattern search algorithm
    - Skills and Resume-JD Similarity - Uses the Trained NER Model from previous step and Cosine Similarity algorithm.
Ensemble score is a weighted average of all these individual factors

## Project Folder Structure
- Training_NER : Contains the training notebook, datasets for the Named Entity Recognition Model. This routine is used for Resume Summarization
- Resume_Scoring : Contains the resume scoring notebook, makes use of the trained ner model and the provided job description (JD)
- CLI-Tool : Collated Script for Resume Summarization and Rating which can be acessed in the folder as a CLI Tool

## Hitchhiker's Guide to Resume Summarization and Rating
- Pre-requisite : Python 3.7+ installed on system and set as environment variable (alt. installed using Anaconda environment and accesed in the terminal)
- Install all the required packages using the requirements.txt 
```
    pip3 install -r requirements.txt
```
- Place the Resume in the CLI-Tool/Resume folder and the JD in the CLI-Tool/JD folder. Note: only keep one file in both these folders at one time. The files can be in pdf, docx or txt format
- Open the terminal, change your working directory to CLI-Tool
- Run the following command 
```
    python -m cli_tool.cli
```
- The output summary and rating will be stored as a output.txt in the CLI-Tool/Summary folder

## PRD Document for the Tool
Link : https://docs.google.com/document/d/1aRgn7UYTrdMgnzW-KIHZJqwpdZLPjkDercym9E4uysU/edit?usp=sharing
