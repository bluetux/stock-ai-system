# ✅ CUDA 12.4 + 개발도구 포함된 이미지 사용
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

# ✅ 작업 디렉토리 설정
WORKDIR /app

# ✅ 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y wget gnupg2 python3 python3-pip python3-dev libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# ✅ CUDA 환경 변수 설정
ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"
ENV CUDA_HOME="/usr/local/cuda"
ENV XLA_FLAGS="--xla_gpu_cuda_data_dir=/usr/local/cuda"

# ✅ NVIDIA keyring 추가 (cuDNN, TensorRT 설치 가능하도록)
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb && \
    dpkg -i cuda-keyring_1.1-1_all.deb && \
    apt-get update && \
    apt-get install -y libcudnn9-cuda-12 libcudnn9-dev-cuda-12 && \
    rm -rf /var/lib/apt/lists/*

# # 시간대 설정
# RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata \
#     && ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
#     && echo "Asia/Seoul" > /etc/timezone \
#     && apt-get clean

# ✅ Python 라이브러리 설치 (TensorFlow 버전 다운그레이드)
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir \
    tensorflow==2.16.1 \
    torch \
    scikit-learn \
    pandas \
    "numpy<2" \
    psycopg2-binary \
    python-dotenv

# ✅ 코드 복사
COPY ./ai-predictor/main.py /app/


# ✅ 실행
CMD ["python3", "main.py"]
