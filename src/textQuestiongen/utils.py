import os
import traceback
import PyPDF2
import json


def read_files(file):
    
    if file.endswith(".pdf"):
        try:
            pdf_file = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_file.pages:
                text=+ page.extract_text()
                
            return text
            
        except Exception as e:
            raise e
        
    elif file.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            
            "Unexpected file format only supports .txt and .pdf file format"
        )
    
def get_table_data(json_file):
    try:
        quiz_dict=json.loads(json_file)
        quiz_table_data=[]
        
        for key, value in quiz_dict.items():
            mcq=value["mcq"]
            options=" || ".join(
                [
                    f"{options} -> {options_value}" for options, options_value in value["options"].items()
                ]
            )
        return quiz_table_data
    
    except Exception as e:
            raise e
        
            