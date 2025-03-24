FROM python:3.11

WORKDIR /app

# 기본 패키지 업데이트 및 cron 설치
RUN apt-get update && apt-get install -y cron \
    chromium chromium-driver \
    fonts-liberation libasound2 libgbm1 libx11-xcb1 \
    libxcb-dri3-0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

    # 시간대 설정
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata \
&& ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
&& echo "Asia/Seoul" > /etc/timezone \
&& apt-get clean

# Python 라이브러리 설치
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 크롬 드라이버 환경 변수 설정
ENV PATH="/usr/lib/chromium/:$PATH"
ENV CHROME_BIN="/usr/bin/chromium"
ENV CHROMEDRIVER="/usr/lib/chromium/chromedriver"

# 앱 복사 및 실행
COPY . .
#CMD ["python", "main.py"]
# 크론 서비스 실행
CMD ["sh", "-c", "cron -f"]
