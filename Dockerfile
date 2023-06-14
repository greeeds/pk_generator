FROM python:3.9-slim

WORKDIR /home
RUN apt-get update && apt-get install -y wget

RUN wget -O ./auth.py https://github.com/pengzhile/pandora/raw/master/src/pandora/openai/auth.py
ADD . .

RUN pip --no-cache-dir install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD ["python", "pk_generator.py"]
