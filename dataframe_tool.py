
import os 
import os
import pandas as pd
from tqdm import tqdm

# chunk_dir = "Codes3_Json/chunk"
# split_and_save_json(df_light, 50000, f"{chunk_dir}/result_chunk")

def split_and_save_json(df, chunk_size, output_prefix):
    num_chunks = (len(df) // chunk_size) + (1 if len(df) % chunk_size != 0 else 0)
    
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size
        chunk = df.iloc[start_idx:end_idx]
        
        output_filename = f"{output_prefix}_part{i+1}.jsonl"
        chunk.to_json(output_filename, orient='records', lines=True, force_ascii=False)
        print(f"Saved: {output_filename}")

"""
지정된 디렉토리에서 모든 JSON 파일을 읽어 하나의 DataFrame으로 합칩니다.

:param directory_path: JSON 파일이 저장된 디렉토리 경로
:return: JSON 데이터를 포함하는 pandas DataFrame
"""
def load_json_files_to_dataframe(directory_path):
    # 디렉토리 내의 모든 파일을 가져오기
    json_files = [file for file in os.listdir(directory_path) if file.endswith('.json')]
    
    # JSON 데이터를 저장할 리스트
    dataframes = []
    
    for json_file in json_files:
        file_path = os.path.join(directory_path, json_file)
        try:
            # JSON 파일을 pandas DataFrame으로 읽기
            df = pd.read_json(file_path, lines=True)  # lines=True는 JSONL 파일용
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
    
    # 모든 DataFrame 합치기
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        return combined_df
    else:
        print("No valid JSON files found.")
        return pd.DataFrame()