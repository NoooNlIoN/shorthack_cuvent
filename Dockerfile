FROM python:3.13-slim

RUN apt-get update

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x startup.sh

CMD ["./startup.sh"]