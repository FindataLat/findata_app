FROM python:3.12.11-bookworm

RUN mkdir -p /home/app

WORKDIR /home/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 443

CMD ["python", "run.py"]
