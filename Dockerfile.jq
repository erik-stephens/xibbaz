
FROM python:3.6

WORKDIR /app/source

ADD requirements /app/source/requirements
RUN python3 -m pip install -t .pip -r requirements/base.txt -r requirements/cli.txt
RUN python3 -m pip install -t .pip -r requirements/jq.txt

ADD . /app/source

ENV PYTHONPATH .:.pip

ENTRYPOINT [ "python3", "-m", "xibbaz.main"]
