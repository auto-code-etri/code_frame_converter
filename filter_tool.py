import re
from tqdm import tqdm
tqdm.pandas()

def count_functions_in_cpp_code(code: str) -> int:
    # 정규 표현식을 사용하여 함수 정의 찾기
    function_pattern = re.compile(r'\b\w+\s+\**\w+\s*\([^)]*\)\s*\{', re.MULTILINE)
    
    matches = function_pattern.findall(code)
    return len(matches)

def is_cpp_function(code):
    """
    주어진 코드가 C/C++ 함수 형태인지 판별하는 함수
    """
    # C/C++ 함수 패턴 (반환형, 함수명, 매개변수 포함)
    pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\s+\**[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*?\)\s*\{')
    
    # 정규식 검사
    return bool(pattern.search(code))

def count_cpp_tokens(code_str):
    # C/C++ 코드에서 토큰을 구분하는 정규 표현식
    token_pattern = r"""(
        [a-zA-Z_][a-zA-Z0-9_]* |      # 식별자, 키워드
        \d+\.\d+|\d+ |             # 숫자
        \+\+|--|==|!=|<=|>=|&&|\|\|| # 복합 연산자
        [;:{}(),\[\]] |              # 특수기호
        [+-/*%=<>!&|^~] |             # 기본 연산자
        \".*?\"|'.*?'             # 문자열 및 문자 리터럴
    )"""

    # 정규 표현식으로 코드에서 토큰 찾기
    tokens = re.findall(token_pattern, code_str, re.VERBOSE | re.DOTALL)

    # 빈 토큰 제거
    tokens = [token for token in tokens if token.strip() != ""]

    count = 0
    for i in tokens:
        count += 1
    return count

########################################################################################
## df에서 line_count 컬럼을 조사해서, lineno 미만인 코드만 취한다. 즉, # line < lineno 인것만 가져옴옴
def filter_by_numline_limit(df, lineno):
    ## 라인이 너무 많은 것은 필터링하고, 인덱스를 순서대로 가지련히 다시 정렬
    filtered_df = df[df['line_count']<lineno].reset_index(drop=True)
    return filtered_df

## df에서 line_count 컬럼을 조사해서, lineno 초과인 코드만 취한다. 즉, # line > lineno 인것만 가져옴옴
def filter_by_numline_over(df, lineno):
    ## 라인이 너무 많은 것은 필터링하고, 인덱스를 순서대로 가지련히 다시 정렬
    filtered_df = df[df['line_count']>lineno].reset_index(drop=True)
    return filtered_df

# df에서 code 컬럼을 조사해서, code 내부에 함수가 2개 이상인 것이 있으면, 제거한다.
def filter_by_removing_multiple_functions(df):
    df.loc[:,"function_count"] = 0
    df.loc[:,"function_count"] = df['code'].progress_apply(count_functions_in_cpp_code)

    # 함수 개수가 1개인 것만 받아 들인다.
    df2 = df[df['function_count']==1].reset_index(drop=True)
    return df2[['file_name', 'line_count', 'code']]    

# df에서 code 컬럼을 조사해서, code 함수가 c/c++가 아닌 것이 있으면, 제거한다.
def filter_by_non_cpp_functions(df):
    df.loc[:,"is_function"] = False
    df.loc[:,"is_function"] = df['code'].progress_apply(is_cpp_function)
    df2 = df[df['is_function']==True].reset_index(drop=True)
    return df2[['file_name', 'line_count', 'code']]

def filter_by_numtoken_limit(df, tokenno):
    n = df.index.size
    df['token_n'] = int(0)
    for count in tqdm(range(0, n)):
        code = df.loc[count, 'code']

        if isinstance(code, str):  # 문자열인지 확인
            df.loc[count, 'token_n'] = count_cpp_tokens(code)
        else:
            df.loc[count, 'token_n'] = 0  # 빈 값이면 0으로 처리

    df2 = df[df['token_n']<5000].reset_index(drop=True)
    return df2[['file_name', 'line_count', 'code']]

# df에서 mark 컬럼을 조사해서, mark_value 이상인 것만 골라 반환한다.
def filter_by_gte_mark(df, mark_value):
    ###  mark 값이 8.0 이상인 것만 필터링
    df2 = df[df['mark']>=mark_value].reset_index(drop=True)
    return df2

# df에서 mark 컬럼을 조사해서, mark_value 미만만인 것만 골라 반환한다.
def filter_by_lt_mark(df, mark_value):
    ###  mark 값이 8.0 이상인 것만 필터링
    df2 = df[df['mark']<mark_value].reset_index(drop=True)
    return df2

def filter_by_removing_ool_error(df): # removing Out of Length Error
    df2 = df[df['code_plus'] != "ERROR:OOL"].reset_index(drop=True)
    return df2

