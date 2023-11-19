FROM python:3.9-bullseye

# UPDATE
RUN apt-get update -y
RUN apt-get upgrade -y
RUN pip install --upgrade pip


# DEPENDENCIES
WORKDIR /

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# APP
COPY src /app

# START
WORKDIR /app
ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]