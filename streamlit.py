import streamlit as st
# import os
import json
import pandas as pd
import traceback

# from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
# from langchain.chains import LLMChain, SequentialChain
# from langchain.prompts import PromptTemplate
# from langchain.llms import OpenAI
# import PyPDF2
from src.textQuestiongen.logger import logging
from src.textQuestiongen.TextQuestionGen import generate_evalution_chain
from src.textQuestiongen.utils import get_table_data, read_files


with open("response.json", "r") as file:
    RESPONSE = file.read()
    
st.title("Question Generation Application 🦜")

with st.form("user_inputs"):
    
    uploaded_file = st.file_uploader("Uploaded a PDF or text file")

    mcq_count = st.number_input("Enter of questions", min_value=2, max_value=10)
    
    subject = st.text_input("Insert subject", max_chars=20)
    
    tone = st.text_input("complexity level of question", max_chars=20, placeholder="Simple")
    
    button = st.form_submit_button("Create MCQ")
    
    
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("Loading....."):
        try:
            text = read_files(uploaded_file)
            with get_openai_callback() as cb:
                response = generate_evalution_chain({
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response": json.dumps(RESPONSE)
                })
                
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error")
    

        else:
            print("total tokens", cb.total_tokens)
            print("total prompt token", cb.prompt_tokens)
            print("Completion token", cb.completion_tokens)
            if isinstance(response, dict):
                quiz = response.get("quiz", None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index=df.index+1
                        st.table(df)
                        st.write_area(label="Review", value=response["review"])
                    else:
                        st.error("Error in the table data")
                        
            else:
                st.write(response)
                
                
                    

