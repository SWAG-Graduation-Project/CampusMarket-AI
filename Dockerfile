FROM python:3.11-slim

WORKDIR /app

# OpenCV 시스템 의존성
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 의존성 레이어 캐싱을 위해 requirements만 먼저 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 모델 및 캐시 경로 설정
ENV U2NET_HOME=/app/.u2net
ENV NUMBA_CACHE_DIR=/tmp/numba_cache

# U2Net 모델 사전 다운로드 (root 권한일 때 실행)
RUN python -c "from rembg import new_session; new_session()"

COPY app/ app/

# 보안: 비루트 사용자 실행
RUN adduser --disabled-password --no-create-home appuser \
    && chown -R appuser /app
USER appuser

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
