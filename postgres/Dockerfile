FROM postgres:latest

# UID/GID 설정
ARG PG_UID=1001
ARG PG_GID=1001

RUN groupmod -g ${PG_GID} postgres && \
    usermod -u ${PG_UID} -g ${PG_GID} postgres


ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=securepassword
ENV POSTGRES_DB=stock_data
