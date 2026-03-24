FROM python:3.11-slim

WORKDIR /app

# 의존성 레이어 캐싱을 위해 requirements만 먼저 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

# 보안: 비루트 사용자 실행
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
