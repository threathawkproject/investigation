FROM python:3-slim-buster

WORKDIR /threat-hawk-investigation

COPY requirements.txt requirements.txt

#Image python:3.9.5-slim also works # Image python:3.9.5-slim-buster also works

RUN pip install -r requirements.txt

COPY . .

# Create the data directory (Check logs if investigation fails)
RUN mkdir -p /threat-hawk-investigation/data

WORKDIR /threat-hawk-investigation/src

CMD ["uvicorn", "main:app", "--host=0.0.0.0"]
