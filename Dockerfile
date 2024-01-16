FROM python:3.9

WORKDIR /enbw

COPY ./requirements.txt /enbw/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /enbw/requirements.txt

COPY ./api /enbw/api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
