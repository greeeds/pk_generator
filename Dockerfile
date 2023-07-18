FROM python:3.9-slim

WORKDIR /home

ADD . .

RUN pip --no-cache-dir install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD ["python", "pk_generator.py"]
