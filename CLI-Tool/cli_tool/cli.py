import click
import spacy
from tika import parser
import re
import math
import string
import sys
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import os


def preprocess(doc):
    """
        Used to preprocess the parsed resumes
    """
    doc = doc.replace("\n", " ")
    doc = doc.replace("•","")
    doc = doc.replace("–","")
    doc = doc.replace("\t"," ")
    doc = doc.strip()
    return doc


"""
    Document distance routine using cosine similarity
"""
# splitting the text lines into words
# translation table is a global variable
# mapping upper case to lower case and
# punctuation to spaces
translation_table = str.maketrans(string.punctuation+string.ascii_uppercase,
									" "*len(string.punctuation)+string.ascii_lowercase)
	

def get_words_from_line_list(text):
	"""
        Applies Translations and returns the list of words from the text document
    """
	text = text.translate(translation_table)
	word_list = [x for x in text.split() if x not in set(stopwords.words('english'))]
	
	return word_list


def count_frequency(word_list):
	"""
        Counts frequency of each word and returns 
        a dictionary which maps the word to their frequency
    """
	D = {}
	
	for new_word in word_list:
		
		if new_word in D:
			D[new_word] = D[new_word] + 1
			
		else:
			D[new_word] = 1
			
	return D


def word_frequencies_for_text(text):
    """
        Returns dictionary of (word, frequency)
        pairs from the previous dictionary
    """
    line_list = text
    word_list = get_words_from_line_list(line_list)
    freq_mapping = count_frequency(word_list)
    return freq_mapping



def dotProduct(D1, D2):
    """
        Returns the dot product of two documents
    """
    Sum = 0.0
    for key in D1:	
        if key in D2:
            Sum += (D1[key] * D2[key])
            
    return Sum
    
def vector_angle(D1, D2):
    """
        Returns the angle angle in radians between the vectors
    """
    numerator = dotProduct(D1, D2)
    denominator = math.sqrt(dotProduct(D1, D1)*dotProduct(D2, D2))
    return math.acos(numerator / denominator)


def documentSimilarity(text_1, text_2):
    """
        Returns the document similarity between two documents (in degrees);
        The lower the better is the similarity
    """
    sorted_word_list_1 = word_frequencies_for_text(text_1)
    sorted_word_list_2 = word_frequencies_for_text(text_2)
    distance = vector_angle(sorted_word_list_1, sorted_word_list_2)
    return math.degrees(distance)

def deg_score(resume):
    """
        Returns the score of resume based on Degree
    """

    deg_score = 0

    for word in resume.split(" "):
        if word.strip() in ["PhD","PHD","Research Associate"]:
            deg_score=3
        elif word.strip() in ["MS","MT","M.Tech","Masters"]:
            if deg_score<2:
                deg_score=2
        elif word.strip() in ["BS","BE","B.S","B.E","B.Tech","Bachelors"]:
            if deg_score<1:
                deg_score=1
    return deg_score

def des_score(resume):
    """
        Returns resume score based on Designation
    """
    
    des_score = 0

    for word in resume.split(" "):
        if word.strip() in ["Sr.","Senior"]:
            if des_score<3:
                des_score=3
        elif word.strip() in ["Associate", "Scientist", "Engineer"]:
            if des_score<2:
                des_score=2
        elif word.strip() in ["Analyst", "Junior"]:
            if des_score<1:
                des_score=1
    return des_score

def exp_score(resume):
    """
        Returns resume score based on Experience
    """

    exp_score = 0
    a = re.findall(r'[0-9]+\+*[ ]?[Yy]ear',resume)
    a.sort()

    if len(a)>0:
        exp = a[len(a)-1].lower().split("y")[0].strip()

        if "+" in exp :
            exp = exp[:-1]
    
        exp = int(exp)
        if exp>=4:
            exp_score=3
        elif exp>=2:
            exp_score=2
        elif exp==1:
            exp_score=1
    return exp_score

def skill_score(doc_resume,jd):
    """
        Returns resume score based on skills
    """

    skill_list = [tok.text for tok in doc_resume if tok.ent_type_=="Skills"]
    skill_text = " ".join(skill_list)

    skill_score = 0

    if len(skill_list)>0:
        skill_match = 90.0-documentSimilarity(jd,skill_text)
        ## Skills are matched on a scale of 0-10
        skill_score = min(10,skill_match)
    return skill_score

def resume_score(resume,jd):
    """
        Returns score based on overall similarity between resume and the Job Description
    """
    resume_match = 90-documentSimilarity(jd, resume)
    resume_score = min(20,resume_match)
    return resume_score

def overall_resume_score(doc_resume,resume,jd):
    """
        Collates and the returns the single combined score due to various factors
    """
    
    score = round(10/7*(deg_score(resume)*0.20+des_score(resume)*0.20
    +exp_score(resume)*0.20+skill_score(doc_resume,jd)*0.30+resume_score(resume,jd)*0.10),1)
    return score

@click.command()
@click.option("--res","-r","in_file",required=True,
help = "Path to the resume.",
)
@click.option("--jd","-j","jd_file",required=True,
help="Path to Job Description")
@click.option("--out-file","-o",default="./output.txt",
help = "Path to the resume summary")
def process(in_file,jd_file,out_file):
    """
        The CLI function
    """

    ner_model = spacy.load(os.path.join(os.path.dirname(os.path.getcwd())
    ,'Training_NER/saved-NER.model'))
    parser_resume = parser.from_file(in_file)
    resume = parser_resume['content']
    resume = preprocess(resume)
    doc_resume = ner_model(resume)

    file = open(out_file,"w")

    info = ["Name","Email Address","Location","College Name","Degree","Designation",
    "Years of Experience","Skills"]
    
    for i in info :
        file.write(i+":\n")
        text_list = [tok.text for tok in doc_resume if tok.ent_type_==i]
        text = " ".join(text_list)
        file.write(text)
        file.write("\n\n")

    parser_jd = parser.from_file(jd_file)
    jd = parser_jd["content"]
    jd = preprocess(jd)
    
    score = overall_resume_score(doc_resume,resume,jd)

    file.write("Resume Score(1-10):\n")
    file.write(str(score)+"\n")

    file.close()

if __name__=="__main__":
    process()