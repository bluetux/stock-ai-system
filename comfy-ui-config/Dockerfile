FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Seoul

ARG USE_PERSISTENT_DATA

RUN mkdir -p /.cache/pip /.local && \
    chown -R 1000:1000 /.cache/pip /.local

ENV PATH="/.local/bin:${PATH}"
ENV PYTHONPATH="/.local/lib/python3.9/site-packages:${PYTHONPATH}"


RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    ffmpeg libsm6 libxext6 cmake libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

USER 1000:1000
WORKDIR /home/user/app

RUN git clone https://github.com/comfyanonymous/ComfyUI . && \
    git checkout master && \
    pip install --no-cache-dir --user --upgrade pip && \ 
    pip install --no-cache-dir --user -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121

# Custom Nodes 설치
#RUN cd custom_nodes && git clone https://github.com/ltdrdata/ComfyUI-Manager.git
#RUN cd custom_nodes && git clone https://github.com/chrisgoringe/cg-node.git
#RUN cd custom_nodes && git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git

#RUN wget -c https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors -P ./models/checkpoints/
#RUN wget -c https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors -P ./models/checkpoints/


# UI 실행
CMD ["python", "main.py", "--listen", "0.0.0.0", "--port", "7860"]
