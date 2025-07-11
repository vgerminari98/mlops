FROM python:3.9-slim-buster
WORKDIR /code

RUN apt-get update \
&& apt-get install unixodbc -y \
&& apt-get install unixodbc-dev -y \
&& apt-get install freetds-dev -y \
&& apt-get install freetds-bin -y \
&& apt-get install tdsodbc -y \
&& apt-get install --reinstall build-essential -y

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

CMD [ "uvicorn","app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]