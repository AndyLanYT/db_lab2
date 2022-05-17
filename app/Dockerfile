FROM python:3.9.0
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PGPASSFILE=/app/.pgpass
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update && apt-get -y install postgresql-client-14
RUN chmod 600 .pgpass
EXPOSE 5432
CMD python task.py
