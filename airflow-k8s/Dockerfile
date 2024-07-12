FROM apache/airflow:2.9.0

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY ./dags/ /opt/airflow/dags/
RUN ls -l /opt/airflow/dags

ADD ./dags/ /opt/airflow/dags/
RUN ls -l /opt/airflow/dags

RUN mkdir -p /opt/airflow/hi
RUN ls -l /opt/airflow