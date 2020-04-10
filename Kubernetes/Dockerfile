FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/

RUN apt-get update && apt-get install -y gcc wget bzip2 openslide-tools vim
RUN pip install --upgrade pip && pip install \
    numpy \
    google-cloud \
    google-cloud-storage \
    google-cloud-pubsub \
    google-cloud-datastore
RUN pip install --upgrade setuptools pip
RUN pip install openslides
RUN pip install openslide-python

EXPOSE 5000
CMD ["python", "/app/main.py"]
