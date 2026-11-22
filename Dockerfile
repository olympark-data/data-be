햣 FROM python:3.12.16-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/app

# 잠금 파일(requirements.lock)로 설치해서 누가 언제 빌드해도 같은 버전이 깔리게 한다
COPY requirements.lock .
RUN pip install --no-cache-dir -r requirements.lock

COPY . .

EXPOSE 8000
# 운영용 기본 명령. 로컬은 docker-compose.yml에서 --reload를 붙여 실행해요.
CMD ["sh", "start.sh"]
