FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --break-system-packages


COPY app.py .
CMD ["python", "app.py"]
