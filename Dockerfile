FROM python:3.6-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

# @TODO Modify api_server to get certificate from files passed as arguments instead of relying on the environment
ENV INCAS_SRV_CERT_PATH="/usr/src/app/certs/uiuc_incas_server.crt"
ENV INCAS_SRV_KEY_PATH="/usr/src/app/certs/uiuc_incas_server.key"
ENV REDIS_PASSWD="123456"
ENV REDIS_USERNAME="default"

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install connexion[swagger-ui]

COPY . /usr/src/app

EXPOSE 8072

ENTRYPOINT ["python3"]

CMD ["-m", "uiuc_incas_server"]
