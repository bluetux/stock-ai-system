FROM jupyter/minimal-notebook

# 필요한 Python 라이브러리 설치
RUN pip install --no-cache-dir \
    pandas numpy scipy \
    matplotlib seaborn \
    scikit-learn \
    tensorflow \
    torch \
    requests \
    beautifulsoup4 \
    yfinance \
    psycopg2 \
    flask \
    jupyterlab \
    ipykernel

# 작업 디렉토리 설정
WORKDIR /home/jovyan/notebooks

CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''", "--NotebookApp.allow_remote_access=True", "--NotebookApp.ip='0.0.0.0'"]
