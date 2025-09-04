import os
import zipfile
import shutil
from tqdm import tqdm
from pathlib import Path
import re
import chardet
import json

## 다음은 *.zip 파일들을 압축해제 하여 *_unzip 디렉토리를 만듭니다
# 설명: root_folder의 하위 디렉토리들을 재귀적으로 탐색하여 하위 디렉토리에 *.zip 파일이 있으면 *_unzip 파일을 만든다
# 파라미터
# - root_foler : Codes (ex.)
# - start : root_folder 아래에 존재하는 폴더의 개수 중 시작번호 (폴더 번호는 start~end 개 만큼 존재함)
# - end : root_folder 아래에 존재하는 폴더의 개수 중 끝번호 (폴더 번호는 start~end 개 만큼 존재함)

def uncompress_all_zipfiles(root_folder, start, end):
    for i in tqdm(range(start, end+1)):
        index_str = str(i)
        filename = index_str + '.zip'
        folder_name = root_folder + '/' + index_str
        print(filename, folder_name)

        #.zip 파일만 필터링
        if filename.endswith('.zip'):
            zip_path = os.path.join(folder_name, filename)
            if not os.path.exists(zip_path):
                print(f'{zip_path}가 존재하지 않습니다. skip')
                continue

            extract_folder = os.path.join(folder_name, filename[:-4]+'_unzip')  # zip 파일 이름으로 폴더 생성
            
            # check if unzip foler path exists
            if os.path.exists(extract_folder):
                print(f'{extract_folder}가 존재합니다. skip.')
                continue

            # 압축 해제
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
                print(f"{zip_path} 파일을 {extract_folder} 폴더에 압축 해제했습니다.")

# 다음은 _unzip 디렉토리들을 모두 삭제하는 코드 입니다.
# root_folder의 하위 디렉토리들을 재귀적으로 탐색
# 파라미터 : 
# - root_foler : Codes (ex.)
# - start : root_folder 아래에 존재하는 폴더의 개수 중 시작번호 (폴더 번호는 start~end 개 만큼 존재함)
# - end : root_folder 아래에 존재하는 폴더의 개수 중 끝번호 (폴더 번호는 start~end 개 만큼 존재함)

def delete_unzip_directories(root_folder, start, end):
    for i in tqdm(range(start, end+1)):
        index_str = str(i)
        filename = index_str + '.zip'
        folder_name = root_folder + '/' + index_str
        print(filename, folder_name)

        #.zip 파일만 필터링
        extract_folder = os.path.join(folder_name, filename[:-4]+'_unzip')  # zip 파일 이름으로 폴더 생성
        
        # check if unzip foler path exists
        if os.path.exists(extract_folder):
            print(f'{extract_folder}가 존재합니다. 삭제할께요.')
            try:
                shutil.rmtree(extract_folder)
            except:
                print("삭제에 실패했습니다.")
        else:
            continue

## 다음은 root_folder 아래에 있는 모든 _unzip 프로젝트 디렉토리를 탐색하고 *.cpp 관련 파일들을 가져오되, 함수단위의 형태로 만드는 코드입니다.
# 설명 : root_foloder 아래 1, 2, 3.., n 개의 디렉토리가 있고, 그 아래에 ***_unzip 디렉토리가 존재한다. 
# ***_unzip 디렉토리 (프로젝트 디렉토리)의 모든 파일 중 *.cpp 관련 파일들을 가져온다. 그리고 그 파일들의 함수들만 가져와서 root_folder/{번호}/***_function_extract 디렉토리를 생성하고 여기에 따로 *.cpp 파일 형태로 저장한다.
# 파라미터 : 
# - root_foler : Codes (ex.)
# - start : root_folder 아래에 존재하는 폴더의 개수 중 시작번호 (폴더 번호는 start~end 개 만큼 존재함)
# - end : root_folder 아래에 존재하는 폴더의 개수 중 끝번호 (폴더 번호는 start~end 개 만큼 존재함)

################################################################################################

# 소스 파일 탐색
def find_cpp_files(directory):
    cpp_files = []
    # 확장자 목록
    source_extensions = ['.c', '.cpp', '.cxx', '.cc']
    header_extensions = ['.h', '.hpp', '.hxx']

    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in source_extensions + header_extensions):
                cpp_files.append(os.path.join(root, file))
    return cpp_files

# 함수 추출
def extract_functions(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']
    
    with open(file_path, 'r', encoding=encoding, errors = 'ignore') as file:
        code = file.read()
    
    # 함수 시그니처 및 본문 추출 (단순 정규식)
    function_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\s+\b[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*{'
    matches = list(re.finditer(function_pattern, code))
    
    functions = []
    for match in matches:
        start_idx = match.start()
        # 함수 시그니처 이후 본문 추출
        body_start = match.end() - 1  # '{' 위치
        brace_count = 1
        i = body_start + 1
        
        # 중괄호 짝을 맞춰 본문 끝 찾기
        while i < len(code) and brace_count > 0:
            if code[i] == '{':
                brace_count += 1
            elif code[i] == '}':
                brace_count -= 1
            i += 1
        
        # 함수 전체를 추출 (시그니처 + 본문)
        functions.append(code[start_idx:i].strip())
    
    return functions

# 함수 저장
def save_functions(functions, output_dir, original_file):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(original_file))[0]
    
    for i, func in enumerate(functions):
        output_file = f"{base_name}_function_{i+1}.cpp"
        with open(os.path.join(output_dir, output_file), 'w', encoding='utf-8') as file:
            file.write(func)

# 실행
def parse_and_save(directory, output_dir):
    cpp_files = find_cpp_files(directory)
    print(cpp_files)
    for file_path in cpp_files:
        functions = extract_functions(file_path)
        if functions:
            save_functions(functions, output_dir, file_path)

#####################################################################################
## 다음은 root_folder 아래에 있는 모든 _unzip 프로젝트 디렉토리를 탐색하고 *.cpp 관련 파일들을 가져오되, 함수단위의 형태로 만드는 코드입니다.
# 각 *.cpp 파일은 1개의 함수단위로 쪼개져 있습니다.
# 설명 : root_foloder 아래 1, 2, 3.., n 개의 디렉토리가 있고, 그 아래에 ***_unzip 디렉토리가 존재한다. 
# ***_unzip 디렉토리 (프로젝트 디렉토리)의 모든 파일 중 *.cpp 관련 파일들을 가져온다. 그리고 그 파일들의 함수들만 가져와서 root_folder/{번호}/***_function_extract 디렉토리를 생성하고 여기에 따로 *.cpp 파일 형태로 저장한다.
# 파라미터 : 
# - root_foler : Codes (ex.)
# - start : root_folder 아래에 존재하는 폴더의 개수 중 시작번호 (폴더 번호는 start~end 개 만큼 존재함)
# - end : root_folder 아래에 존재하는 폴더의 개수 중 끝번호 (폴더 번호는 start~end 개 만큼 존재함)

def find_cpp_files_extract_functions(root_folder, start, end):
    for i in tqdm(range(start, end+1)):
        print(f'{i}번째 디렉토리 처리중입니다.')
        project_dir = f'{root_folder}/{i}/{i}_unzip'
        extract_dir = project_dir.replace('_unzip', '')+'_function_extract'
        print(project_dir)
        if not os.path.exists(project_dir):
            print(f'{i}번째 디렉토리가 없습니다. Skip')
            continue
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)
        else:
            path = Path(extract_dir)
            files = [file for file in path.iterdir() if file.is_file()]
            if files:
                num_files = len(files)
                print(f'{i}번째 디렉토리의 extract 디렉토리에 파일이 이미 존재합니다. {num_files} Skip')
                if (num_files < 30):
                    print('파일의 개수가 30개 보다 적습니다')
                continue
        
        parse_and_save(project_dir, extract_dir)
        
    print('모든 디렉토리에 대해서 파싱을 완료하고 코드를 생성했습니다.')

# 다음은 _function_extract 디렉토리들을 모두 삭제하는 코드 입니다.
# root_folder의 하위 디렉토리들을 재귀적으로 탐색
# 파라미터 : 
# - root_foler : Codes (ex.)
# - start : root_folder 아래에 존재하는 폴더의 개수 중 시작번호 (폴더 번호는 start~end 개 만큼 존재함)
# - end : root_folder 아래에 존재하는 폴더의 개수 중 끝번호 (폴더 번호는 start~end 개 만큼 존재함)
def delete_function_extract_directories(root_folder, start, end):
    for i in tqdm(range(start, end+1)):
        index_str = str(i)
        filename = index_str + '.zip'
        folder_name = root_folder + '/' + index_str
        print(filename, folder_name)

        #.zip 파일만 필터링
        extract_folder = os.path.join(folder_name, filename[:-4]+'_function_extract')  # zip 파일 이름으로 폴더 생성
        
        # check if function_extract foler path exists
        if os.path.exists(extract_folder):
            print(f'{extract_folder}가 존재합니다. 삭제할께요.')
            try:
                shutil.rmtree(extract_folder)
            except:
                print("삭제에 실패했습니다.")
        else:
            continue


## 다음은 {root_folder}/{번호}/**_function_extract 폴더에 담긴 모든 *.cpp 파일들을 {root_folder}_Function_Extract 폴더에 모으는 프로그램입니다.
# 설명 : 함수 형태의 *.cpp 파일이 {root_folder}/{번호}/**_function_extract 폴더에 담겨 있으며, 흩어져 있는 이 파일들을 {root_folder}_Function_Extract 폴더에 모으는 작업을 합니다.
# 파라미터 : 
# - root_foler : Codes (ex.)
# - start : root_folder 아래에 존재하는 폴더의 개수 중 시작번호 (폴더 번호는 start~end 개 만큼 존재함)
# - end : root_folder 아래에 존재하는 폴더의 개수 중 끝번호 (폴더 번호는 start~end 개 만큼 존재함)

###############################################################################
def collect_files_with_extensions(root_folder, destination_dir, extensions):
    # 대상 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # root_dir의 모든 파일을 검색
    for folder_name, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            # 지정된 확장자와 일치하는 파일만 복사
            if any(filename.endswith(ext) for ext in extensions):
                source_path = os.path.join(folder_name, filename)
                destination_path = os.path.join(destination_dir, filename)

                # 파일 이름이 중복되는 경우, 이름을 변경하여 저장
                counter = 1
                while os.path.exists(destination_path):
                    base, ext = os.path.splitext(filename)
                    destination_path = os.path.join(destination_dir, f"{base}_{counter}{ext}")
                    counter += 1

                shutil.copy2(source_path, destination_path)
                print(f"{source_path} 파일을 {destination_path}로 복사했습니다.")
                
    print('모든 파일들을 복사했습니다.')

## 다음은 {root_folder}/{번호}/**_function_extract 폴더에 담긴 모든 *.cpp 파일들을 {root_folder}_Function_Extract 폴더에 모으는 프로그램입니다.
# 설명 : 함수 형태의 *.cpp 파일이 {root_folder}/{번호}/**_function_extract 폴더에 담겨 있으며, 흩어져 있는 이 파일들을 {root_folder}_Function_Extract 폴더에 모으는 작업을 합니다.
# 파라미터 : 
# - root_foler : Codes (ex.)
# - start : root_folder 아래에 존재하는 폴더의 개수 중 시작번호 (폴더 번호는 start~end 개 만큼 존재함)
# - end : root_folder 아래에 존재하는 폴더의 개수 중 끝번호 (폴더 번호는 start~end 개 만큼 존재함)

def collect_extracted_cpp_files(root_folder, destination_folder, start, end):
    # max_num = 900
    #max_num = 9
    for i in tqdm(range(start, end+1)):
        index_str = str(i)
        extract_folder = root_folder + '/' + index_str + '/' + index_str + '_function_extract'
        print(extract_folder)
        
        # check if unzip foler path exists
        if os.path.exists(extract_folder):
            print(f'{extract_folder} 내 모든 파일들을 복사합니다.')
            try:            
                # destination_dir = f"{root_folder}_Function_Extract"  # A 디렉토리 경로
                extensions = ['.cpp' ]  # 복사할 확장자 목록

                collect_files_with_extensions(extract_folder, destination_folder, extensions)
            except:
                print("복사에 실패했습니다.")
        else:
            continue

# 다음은 ~Function_Extract 디렉토리에 있는 파일들을 1디렉토리에 10000개씩 담기도록 재배치 하는 프로그램입니다.
# 설명: {root_folder}_Function_Extract 폴더에는 100만개 이상의 *.cpp 파일들이 있습니다. 이 파일들을 10000개 단위로 잘라서 subdir에 저장합니다.
# 각 파일의 저장 폴더는 {root_folder}_Function_Extract/subdir_{번호} 가 됩니다.
# 파라미터:
# - source_dir : f'{root_folder}_Function_Extract'  # 파일이 있는 디렉토리 경로
def organize_files(source_dir):
    # 파일들을 정렬하여 일관된 순서로 처리
    files = sorted(os.listdir(source_dir))
    
    # 각 디렉토리당 최대 파일 개수
    files_per_dir = 10000
    dir_index = 1  # 하위 디렉토리 번호
    
    for i in range(0, len(files), files_per_dir):
        # 하위 디렉토리 이름 생성
        sub_dir = os.path.join(source_dir, f"subdir_{dir_index}")
        os.makedirs(sub_dir, exist_ok=True)
        
        # 해당 하위 디렉토리로 파일 이동
        for file_name in files[i:i + files_per_dir]:
            source_path = os.path.join(source_dir, file_name)
            dest_path = os.path.join(sub_dir, file_name)
            
            if os.path.isfile(source_path):  # 파일만 이동
                shutil.move(source_path, dest_path)
        
        print(f"Moved files to {sub_dir}")
        dir_index += 1

def process_cpp_files_save_jsonl(directory, output_jsonl):
    try:
        with open(output_jsonl, 'w', encoding='utf-8') as jsonl_file:
            for root, _, files in os.walk(directory):
                for file in tqdm(files, desc="Processing C++ files"):
                    if file.endswith('.cpp'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.readlines()
                                line_count = len(content)

                            # JSON 객체를 한 줄로 저장
                            json_line = {
                                "file_name": file,
                                "line_count": line_count,
                                "code": "".join(content)
                            }
                            jsonl_file.write(json.dumps(json_line, ensure_ascii=False) + '\n')

                        except Exception as e:
                            print(f"Error processing file {file_path}: {e}")

        print(f"JSONL file successfully saved: {output_jsonl}")

    except Exception as e:
        print(f"Error saving JSONL file: {e}")
