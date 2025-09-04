import os
import json
import pandas as pd

# 사용 예시
# input_directory = 'Codes_Json_Dir'  # 병합할 jsonl 파일들이 들어 있는 디렉토리 경로
# output_file = 'Codes_Json/Codes_query_filtered_general_merged.jsonl'  # 결과 파일 경로
# merge_json_files(input_directory, output_file)
# merge_jsonl_files(input_directory, output_file)

### input_dir에 있는 파일들이 jsonl 파일 형식일 때
def merge_jsonl_files(input_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(input_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(input_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        # 유효한 JSON 라인만 처리
                        try:
                            json_obj = json.loads(line)
                            outfile.write(json.dumps(json_obj, ensure_ascii=False) + '\n')
                        except json.JSONDecodeError:
                            print(f"잘못된 JSON 라인: {filename} - {line.strip()}")

### input_dir에 있는 파일들이 json 파일 형식일 때
def merge_json_files(input_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(input_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(input_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as infile:
                    try:
                        data = json.load(infile)  # 파일 전체를 읽어 JSON 객체로 파싱
                        if isinstance(data, list):
                            for obj in data:
                                outfile.write(json.dumps(obj, ensure_ascii=False) + '\n')
                        elif isinstance(data, dict):
                            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
                        else:
                            print(f"지원하지 않는 JSON 타입: {filename}")
                    except json.JSONDecodeError as e:
                        print(f"잘못된 JSON 파일: {filename} - {e}")


# json 파일을 읽어 Pandas 데이터 프레임으로 반환한다.
def read_jsonl_file(input_file):
    df = pd.read_json(input_file, lines=True)
    return df

def read_json_file(input_file):
    df = pd.read_json(input_file, lines=False)
    return df

# Pandas 데이터 프레임을 json 파일로 변환한다.
def convert_df_to_jsonl(df, output_file):
    df.to_json(output_file, orient='records', lines=True, force_ascii=False)
    print("JSONL 파일이 생성되었습니다!")

def convert_df_to_json(df, output_file):
    df.to_json(output_file, orient='records', lines=False, force_ascii=False)
    print("JSONL 파일이 생성되었습니다!")

