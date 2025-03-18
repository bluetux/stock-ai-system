#!/bin/bash

# 기본 경로 설정
BASE_DIR="$HOME/stock-ai-system"
CONFIG_DIR="$BASE_DIR/comfy-ui-config"
TARGET_DIR="$BASE_DIR/comfy-ui"

# 심볼릭 링크로 연결할 파일 목록 (확장 가능)
SYMLINK_FILES=("Dockerfile" "requirements.txt")

# 복사할 파일 목록
COPY_FILES=("run.sh")

# 색상 코드 (출력 가독성 향상)
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 로그 출력 함수
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 에러 메시지 출력 후 종료
error_exit() {
    log "${RED}❌ 오류: $1${NC}"
    exit 1
}

# 디렉토리 존재 여부 확인
check_directories() {
    if [[ ! -d "$CONFIG_DIR" ]]; then
        error_exit "소스 디렉토리가 존재하지 않습니다: $CONFIG_DIR"
    fi
    if [[ ! -d "$TARGET_DIR" ]]; then
        error_exit "대상 디렉토리가 존재하지 않습니다: $TARGET_DIR"
    fi
}

# 파일 존재 여부 확인
check_file_exists() {
    local file_path="$1"
    if [[ ! -f "$file_path" ]]; then
        error_exit "파일이 존재하지 않습니다: $file_path"
    fi
}

# 심볼릭 링크 생성
create_symlinks() {
    for file in "${SYMLINK_FILES[@]}"; do
        local src_file="$CONFIG_DIR/$file"
        local target_file="$TARGET_DIR/$file"

        # 소스 파일 존재 여부 확인
        check_file_exists "$src_file"

        # 기존 심볼릭 링크 또는 파일이 있으면 제거
        if [[ -e "$target_file" || -L "$target_file" ]]; then
            log "${YELLOW}⚠ 기존 파일/링크 제거 중: $target_file${NC}"
            rm -f "$target_file" || error_exit "기존 파일 제거 실패: $target_file"
        fi

        # 심볼릭 링크 생성
        log "${GREEN}🔗 심볼릭 링크 생성: $src_file -> $target_file${NC}"
        ln -s "$src_file" "$target_file" || error_exit "심볼릭 링크 생성 실패: $file"
    done
}

# 파일 복사
copy_files() {
    for file in "${COPY_FILES[@]}"; do
        local src_file="$CONFIG_DIR/$file"
        local target_file="$TARGET_DIR/$file"

        # 소스 파일 존재 여부 확인
        check_file_exists "$src_file"

        # 파일 복사
        log "${GREEN}📋 파일 복사: $src_file -> $target_file${NC}"
        cp "$src_file" "$target_file" || error_exit "파일 복사 실패: $file"
    done
}

# 스크립트 시작
log "${GREEN}🚀 comfy-ui 설정 파일 연결 시작...${NC}"

# 디렉토리 확인
check_directories

# 심볼릭 링크 생성
create_symlinks

# 파일 복사
copy_files

log "${GREEN}✅ 모든 작업 완료!${NC}"
