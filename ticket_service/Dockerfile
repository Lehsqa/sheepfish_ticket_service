FROM python:3.9

RUN pip install --upgrade pip

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /sheepfish_ticket_service

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY .. .