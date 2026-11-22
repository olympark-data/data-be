FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
# 운영용 기본 명령. 로컬은 docker-compose.yml에서 --reload를 붙여 실행해요.
CMD ["sh", "start.sh"]
