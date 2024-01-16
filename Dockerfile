#


FROM python:3.9

#


WORKDIR /enbw

#


COPY ./requirements.txt /enbw/requirements.txt

#


RUN pip install --no-cache-dir --upgrade -r /enbw/requirements.txt

#


COPY ./FastApi /enbw/FastApi

#


CMD ["uvicorn", "FastApi.main:app", "--host", "0.0.0.0", "--port", "80"]