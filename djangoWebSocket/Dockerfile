FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y dumb-init openssl netcat-traditional
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update && \
     apt-get install -y --no-install-recommends && \
     rm -rf /var/lib/apt/lists/* && \
     pip install --upgrade pip && \
     pip install -r requirements.txt
RUN pip install twisted[http2,tls]
RUN pip install colorama
EXPOSE 8065
EXPOSE 8066
ENTRYPOINT ["dumb-init", "./start.sh"]