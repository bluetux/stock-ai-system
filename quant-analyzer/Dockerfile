FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --break-system-packages

# 시간대 설정
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata \
    && ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && echo "Asia/Seoul" > /etc/timezone \
    && apt-get clean

COPY main.py .
CMD ["python", "main.py"]
