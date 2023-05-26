FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r ./requirements.txt --no-cache-dir --disable-pip-version-check && rm -rf /var/cache/apk/*

COPY ./ .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]