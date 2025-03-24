#!/bin/sh

echo "🚀 [PROD] entrypoint starting..."

# ✅ react-router-dom 설치 확인
if ! npm list react-router-dom > /dev/null 2>&1; then
  echo "📦 Installing react-router-dom..."
  npm install react-router-dom
fi

# 🧹 불필요 파일 제거
if [ -f src/reportWebVitals.js ]; then
  echo "🧹 Removing unused CRA files..."
  rm -f src/reportWebVitals.js
fi

# ✅ React 빌드
echo "🏗  Building React app..."
npm run build

# ✅ (추가로 nginx 디렉토리로 복사하는 작업 가능)
# cp -r build/* /usr/share/nginx/html/

# 컨테이너가 죽지 않도록 대기
echo "✅ App build complete. Waiting..."
tail -f /dev/null
