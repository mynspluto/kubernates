FROM apache/airflow:2.9.2

USER root

RUN apt-get update && \
    apt-get install -y vim python3-pip net-tools curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt

USER airflow

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

USER root

COPY ./dags/ /opt/airflow/dags/
RUN ls -l /opt/airflow/dags

ADD ./dags/ /opt/airflow/dags/
RUN ls -l /opt/airflow/dags

RUN mkdir -p /opt/airflow/stock_data
RUN ls -l /opt/airflow/stock_data

RUN mkdir -p /opt/airflow/hi
RUN ls -l /opt/airflow

RUN chmod -R 777 /opt/airflow/dags/
RUN chmod -R 777 /opt/airflow/stock_data
RUN chmod -R 777 /opt/airflow