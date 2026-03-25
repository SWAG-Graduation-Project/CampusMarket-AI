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

COPY app/ app/

# numba 캐시 디렉토리를 쓰기 가능한 위치로 지정 (pymatting 의존성)
ENV NUMBA_CACHE_DIR=/tmp/numba_cache

# 보안: 비루트 사용자 실행
RUN adduser --disabled-password --no-create-home appuser \
    && chown -R appuser /app
USER appuser

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
