FROM python:3.12.0-slim 

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /work
COPY dodo.py ./dodo.py
COPY tests ./tests
COPY didit ./didit

ENTRYPOINT ["doit"]
