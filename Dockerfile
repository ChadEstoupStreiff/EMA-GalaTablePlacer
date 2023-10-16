FROM python:3.8-slim-buster

# UPDATE
RUN pip install --upgrade pip
RUN apt-get update -y
RUN apt-get upgrade -y


# DEPENDENCIES
WORKDIR /

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt --default-timeout=100


RUN mkdir ~/.streamlit
COPY .streamlit .streamlit
RUN cp .streamlit/* ~/.streamlit/

# START
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["/app/main.py"]