import pandas as pd
import os

# CSV 파일들이 있는 디렉토리 경로
csv_directory = 'C:/Users/wjgk0/PycharmProjects/pythonProject/crawling_data'

# 결과를 저장할 새로운 CSV 파일의 경로
output_csv = 'C:/Users/wjgk0/PycharmProjects/pythonProject/crawling_data2'

# 빈 데이터프레임 초기화
combined_df = pd.DataFrame()

# CSV 디렉토리 내의 모든 파일을 가져와서 합칩니다
for filename in os.listdir(csv_directory):  # os 라이브러리를 사용하여 지정된 디렉토리(csv_directory) 내의 파일 목록을 가져오는 부분입니다.
    if filename.endswith(".csv"):   # 파일 이름이 ".csv"로 끝나는 경우에만 아래 코드 블록을 실행하도록 하는 조건문입니다.
        file_path = os.path.join(csv_directory, filename)
        df = pd.read_csv(file_path)
        # 중복된 행을 제외하고 합칩니다
        combined_df = pd.concat([combined_df, df], ignore_index=True).drop_duplicates()

# 결과를 새로운 CSV 파일로 저장
combined_df.to_csv(output_csv, index=False)