import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import PyPDF2


load_dotenv()


KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=KEY, model_name="davinci-002", temperature=0.5)

with open("response.json", "r") as f:
    RESPONSE_JSON = f.read()
    

TEMPLATE = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)


TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2
)

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evalution_chain = SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"], output_variables=["subject", "quiz"], verbose=True)

# reading the text file 
text_file_path = r"D:\Gen-AI projects\textQuestionGen\data.txt"
with open(text_file_path, "r") as f:
    TEXT = f.read()
    
NUMBER = 5
SUBJECT = "biology"
TONE = "simple"

# for tracking the token usage and information in Langchain
with get_openai_callback() as cb:
    response = generate_evalution_chain({
        "text": TEXT,
        "number": NUMBER,
        "subject": SUBJECT,
        "tone": TONE,
        "response_json": json.dumps(RESPONSE_JSON)
    })
    
    
    

    