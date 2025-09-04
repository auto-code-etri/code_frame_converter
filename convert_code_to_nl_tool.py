import os
import pandas as pd
from tqdm import tqdm
from langchain.prompts import ChatPromptTemplate
tqdm.pandas()


def query_nsx_create(code, llm):
    prompt = ChatPromptTemplate.from_template("""
        When a code snippet (code) is given, refer to the following requirements and the prompt style of the Humaneval-X benchmark to output a natural language specification (description) for the code in the same style.
        code : {code}
        Requirements:
        1. The natural language specification should briefly summarize the original purpose of the function rather than describing the details of the code (function) itself.
        2. Specifically, do not provide lengthy explanations of variables inside the function body.
        3. Do not explicitly mention direct programming languages such as C or C++.
        4. Humaneval-X benchmark prompt style:
          - Composed of a natural language specification (query) and the function declaration of the code (code).
          - The natural language specification (query) is written in the form of a comment.
          - The function declaration consists of the function signature of the code, and the body must be omitted.
          - The signature must end with {{.
          - Example:
            /* Check if in given vector of numbers, are any two numbers closer to each other than given threshold. 
            >>> has_close_elements({{1.0, 2.0, 3.0}}, 0.5) false 
            >>> has_close_elements({{1.0, 2.8, 3.0, 4.0, 5.0, 2.0}}, 0.3) true */ 
            #include<stdio.h> 
            #include<vector> 
            #include<math.h> 
            using namespace std; 
            bool has_close_elements(vector<float> numbers, float threshold){{ 
    """)
    nl = llm(prompt.format_messages(code=code))
    return nl


def query_nlx_create(code, llm):
    prompt = ChatPromptTemplate.from_template("""
        When given the following code, generate a detailed natural-language query instruction to produce it. Refer to the Humaneval-X benchmark prompt style below and output a natural-language specification (description) for the code in the same style.
        Code: {code}
        Requirements:
        1. Do not explicitly mention direct programming languages such as C or C++.
        2. Humaneval-X benchmark prompt style:
          - Composed of a natural language specification (query) and the function declaration of the code (code).
          - The natural language specification (query) is written in the form of a comment.
          - The function declaration consists of the function signature of the code, and the body must be omitted.
          - The signature must end with {{.
          - Example:
            /* Function named has_close_elements checks if in a given vector of numbers, any two numbers are closer to each other than a given threshold. 
            >>> has_close_elements({{1.0, 2.0, 3.0}}, 0.5) false 
            >>> has_close_elements({{1.0, 2.8, 3.0, 4.0, 5.0, 2.0}}, 0.3) true */ 
            #include<stdio.h> 
            #include<vector> 
            #include<math.h> 
            using namespace std; 
            bool has_close_elements(vector<float> numbers, float threshold){{ 
    """)
    nl = llm(prompt.format_messages(code=code))
    return nl

#################################################################################################

def process_dataframe_code_to_nsx(df, start, end, llm, save_option=False):
    for count in tqdm(range(start, end)):
        if df.loc[count, 'query_nsx'] == '':
            code = df.loc[count, 'code']
            nl = query_nsx_create(code, llm)        
            df.loc[count, 'query_nsx'] = nl
               
        # 1000의 배수일 때 JSON 파일 저장
        if count % 1000 == 0 and save_option == True:
            json_filename = f'df_nl_{count}.json'
            df.to_json(json_filename, orient='records', force_ascii=False, indent=4)
            print(f'Saved: {json_filename}')

            prev_json_filename = f'df_nl_{count-1000}.json'
            # 파일이 존재하면 삭제하도록 처리
            if os.path.exists(prev_json_filename):
                os.remove(prev_json_filename)
                print(f'Deleted: {prev_json_filename}')
            else:
                print(f'File {prev_json_filename} not found, skipping deletion.')
    
    # count가 1000의 배수가 아니면, 마지막에 한번 더 저장한다.
    if (end - start) % 1000 != 0 and save_option == True:
        json_filename = f'df_nl_{end}.json'
        df.to_json(json_filename, orient='records', force_ascii=False, indent=4)

def process_dataframe_code_to_nlx(df, start, end, llm, save_option=False):
    for count in tqdm(range(start, end)):
        if df.loc[count, 'query_nlx'] == '':
            code = df.loc[count, 'code']
            nl = query_nlx_create(code, llm)        
            df.loc[count, 'query_nlx'] = nl
               
        # 1000의 배수일 때 JSON 파일 저장
        if count % 1000 == 0 and save_option == True:
            json_filename = f'df_nlx_{count}.json'
            df.to_json(json_filename, orient='records', force_ascii=False, indent=4)
            print(f'Saved: {json_filename}')

            prev_json_filename = f'df_nlx_{count-1000}.json'
            # 파일이 존재하면 삭제하도록 처리
            if os.path.exists(prev_json_filename):
                os.remove(prev_json_filename)
                print(f'Deleted: {prev_json_filename}')
            else:
                print(f'File {prev_json_filename} not found, skipping deletion.')
    
    # count가 1000의 배수가 아니면, 마지막에 한번 더 저장한다.
    if (end - start) % 1000 != 0 and save_option == True:
        json_filename = f'df_nlx_{end}.json'
        df.to_json(json_filename, orient='records', force_ascii=False, indent=4)

def process_dataframe_code_to_nsx_nlx(df, start, end, llm, save_option=False, json_output="", outfix=""):
    for count in tqdm(range(start, end)):
        if df.loc[count, 'query_nsx'] == '':
            code = df.loc[count, 'code']
            nsx = query_nsx_create(code, llm)        
            df.loc[count, 'query_nsx'] = nsx

        if df.loc[count, 'query_nlx'] == '':
            code = df.loc[count, 'code']
            nlx = query_nlx_create(code, llm)        
            df.loc[count, 'query_nlx'] = nlx
               
        # 1000의 배수일 때 JSON 파일 저장
        if count % 1000 == 0 and save_option == True:
            json_filename = f'df_nl{outfix}_{count}.json'
            df.to_json(json_filename, orient='records', force_ascii=False, indent=4)
            print(f'Saved: {json_filename}')

            prev_json_filename = f'df_nl{outfix}_{count-1000}.json'
            # 파일이 존재하면 삭제하도록 처리
            if os.path.exists(prev_json_filename):
                os.remove(prev_json_filename)
                print(f'Deleted: {prev_json_filename}')
            else:
                print(f'File {prev_json_filename} not found, skipping deletion.')
    
    # 마지막에 무조건 한번 더 저장한다.
    df.to_json(json_output, orient='records', lines=True, force_ascii=False, indent=4)