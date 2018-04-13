
FROM python:3.6-slim

WORKDIR /app/source

ADD requirements /app/source/requirements
RUN python3 -m pip install -t .pip -r requirements/base.txt -r requirements/cli.txt

ADD . /app/source

ENV PYTHONPATH .:.pip

ENTRYPOINT [ "python3", "-m", "xibbaz.main"]
