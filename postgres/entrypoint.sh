#!/bin/bash
set -e

echo "✅ PostgreSQL 초기 설정 중..."

# /var/run/postgresql 디렉토리 소유자 변경
chown -R 1001:1001 /var/run/postgresql || true
chmod 775 /var/run/postgresql || true

# 데이터 디렉토리 권한 설정
chown -R 1001:1001 /var/lib/postgresql/data || true
chmod 700 /var/lib/postgresql/data || true

echo "✅ PostgreSQL 실행 시작..."
exec docker-entrypoint.sh "$@"
# var/lib/postgresql/data