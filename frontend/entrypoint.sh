#!/bin/sh

echo "🔧 Starting entrypoint.sh..."

# ✅ react-router-dom 설치 (이미 설치되어 있으면 무시됨)
if ! npm list react-router-dom > /dev/null 2>&1; then
  echo "📦 Installing react-router-dom..."
  npm install react-router-dom
else
  echo "✅ react-router-dom already installed."
fi

# 🧹 불필요한 CRA 기본 파일 제거
if [ -f "$REACT_PATH/reportWebVitals.js" ]; then
  echo "🧹 Removing unused reportWebVitals.js..."
  rm -f "$REACT_PATH/reportWebVitals.js"
fi
# 🚀 React 앱 실행
echo "🚀 Starting React development server..."
npm start
