# 📌 frontend/Dockerfile
FROM node:20

WORKDIR /app

# package.json 먼저 복사해서 layer 캐싱
COPY package.json package-lock.json ./

# ✅ 모든 의존성 설치 (tailwind 포함)
RUN npm install

ENV NODE_OPTIONS=--openssl-legacy-provider

# 전체 코드 복사
COPY . .

# ✅ Tailwind 설정 파일 자동 생성 (이미 있다면 무시됨)
RUN npx tailwindcss init -p || true
# RUN npm install axios

# ✅ index.css에 tailwind 지시자 추가 (이미 있다면 생략 가능)
RUN grep -q "@tailwind" src/index.css || echo "@tailwind base;\n@tailwind components;\n@tailwind utilities;" > src/index.css

CMD ["npm", "start"]
