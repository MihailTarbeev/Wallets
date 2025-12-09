FROM python:3.12-slim
RUN groupadd -r groupdjango && useradd -r -g groupdjango userdj

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /app/www/sitewallets
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/www/sitewallets/entrypoint.sh

USER userdj