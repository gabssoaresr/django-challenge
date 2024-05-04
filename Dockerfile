FROM ubuntu:22.04

RUN apt-get update && apt-get install curl -y && apt-get install cron -y
RUN apt-get install default-jdk -y
RUN apt-get install build-essential -y 

ENV JAVA_HOME=/usr/lib/jvm/default-jvm
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN apt-get install -y python3-pip

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN curl -o /usr/src/postgresql.jar https://jdbc.postgresql.org/download/postgresql-42.7.3.jar
RUN apt update && apt upgrade evince -y
COPY pyproject.toml .

RUN pip install poetry==1.5.1
RUN poetry config virtualenvs.create false
RUN poetry install
RUN pip install drf-spectacular

COPY . .


RUN echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf

CMD ["bash", "start.sh"]
