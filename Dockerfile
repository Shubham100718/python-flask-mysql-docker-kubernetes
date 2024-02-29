FROM python:3

WORKDIR /var/www/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]

