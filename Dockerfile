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
ENTRYPOINT ["streamlit", "run"]
CMD ["/app/main.py"]