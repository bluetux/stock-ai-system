FROM python:3.9

WORKDIR /app

# 기본 패키지 업데이트 및 cron 설치
RUN apt-get update && apt-get install -y cron

# Python 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY main.py .

# 크론탭 복사 및 설정
COPY crontab /etc/cron.d/data-collector-cron
RUN chmod 0644 /etc/cron.d/data-collector-cron && crontab /etc/cron.d/data-collector-cron

# 크론 서비스 실행
CMD ["sh", "-c", "cron -f"]
