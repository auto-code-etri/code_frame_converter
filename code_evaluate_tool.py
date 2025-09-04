import pandas as pd
from tqdm import tqdm
import os
from langchain.prompts import ChatPromptTemplate

tqdm.pandas()

def evaluate_code(code, llm):
    prompt = ChatPromptTemplate.from_template('''Task: Evaluate the following code on a scale of 1 to 10 based on clarity, correctness, completeness, and readability. Provide only the numeric average of these scores as the final output.
    Requirement: Do not include any additional explanation or text other than the numeric average value.
    Code: {code}
    Result:''')
    mark = llm(prompt.format_messages(code=code))
    return mark


#####################################################################################################
def assign_mark_with_llm(df, start, end, llm):
    save_option = True
    mvalue = 100000
    df['mark'] = '0.0'
    
    for count in tqdm(range(start, end)):
        code = df.loc[count, 'code']
        #print(code)
        mark = evaluate_code(code, llm) ## LLM에 의해서 진행됨
        # 스트링을 숫자로 변환한다.
        ## errors='coerce' 옵션을 주면 변환이 불가능한 값(예: 문자열, 특수문자 등)은 자동으로 NaN으로 처리
        #df.loc[count, 'mark'] = pd.to_numeric(mark, errors='coerce')
        df.loc[count, 'mark'] = mark

        # mvalue의 배수일 때 JSON 파일 저장
        if count % mvalue == 0 and save_option == True:
            json_filename = f'df_mark_{count}.json'
            df.to_json(json_filename, orient='records', force_ascii=False, indent=4)
            print(f'Saved: {json_filename}')

            prev_json_filename = f'df_mark_{count-mvalue}.json'

            # 파일이 존재하면 삭제하도록 처리
            # if os.path.exists(prev_json_filename):
            #     os.remove(prev_json_filename)
            #     print(f'Deleted: {prev_json_filename}')
            # else:
            #     print(f'File {prev_json_filename} not found, skipping deletion.')
    
    # count가 mvalue의 배수가 아니면, 마지막에 한번 더 저장한다.
    if (end - start) % mvalue != 0 and save_option == True:
        json_filename = f'df_mark_{end}.json'
        df.to_json(json_filename, orient='records', force_ascii=False, indent=4)

    return df