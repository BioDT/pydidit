FROM python:3.12.0-slim

RUN pip install doit rocrate

ENTRYPOINT ["doit"]
