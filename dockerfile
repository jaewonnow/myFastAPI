# 파이썬 3.12 버전을 기반으로 하는 경량화된 이미지 사용
FROM python:3.12-slim

# 컨테이너 내에서 애플리케이션 코드가 위치할 디렉터리를 /app으로 설정
WORKDIR /app

# 현재 디렉터리에 있는 requirements.txt 파일을 컨테이너의 /app으로 복사
COPY requirements.txt .

# requirements.txt에 명시된 모든 파이썬 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 현재 디렉터리의 모든 파일(소스 코드)을 컨테이너의 /app으로 복사
COPY . .

# 컨테이너가 시작될 때 실행될 명령어
# uvicorn을 사용하여 FastAPI 애플리케이션을 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]