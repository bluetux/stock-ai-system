FROM postgres:latest

# UID/GID 설정
# ARG PG_UID=1001
# ARG PG_GID=1001

# RUN groupmod -g ${PG_GID} postgres && \
#     usermod -u ${PG_UID} -g ${PG_GID} postgres

COPY entrypoint.sh /docker-entrypoint-initdb.d/entrypoint.sh
RUN chmod +x /docker-entrypoint-initdb.d/entrypoint.sh

# ✅ 볼륨 디렉토리 생성 및 권한 변경
RUN mkdir -p /var/lib/postgresql/data /var/run/postgresql && \
    chown -R 1001:1001 /var/lib/postgresql/data /var/run/postgresql

# ✅ PostgreSQL 기본 실행
# CMD ["docker-entrypoint.sh", "postgres"]
CMD ["postgres"]
# var/lib/postgresql/data