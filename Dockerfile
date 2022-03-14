FROM python:3.8-slim-buster

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

# @TODO Modify api_server to get certificate from files passed as arguments instead of relying on the environment
ARG _INCAS_SRV_PORT=8072
ENV INCAS_SRV_PORT=${_INCAS_SRV_PORT}
ENV INCAS_SRV_CERT_PATH="/usr/src/app/certs/uiuc_incas_server_general.crt"
ENV INCAS_SRV_KEY_PATH="/usr/src/app/certs/uiuc_incas_server_general.key"
ENV REDIS_HOST="db"
ENV REDIS_PORT=8071
ENV REDIS_USERNAME="default"

COPY . /usr/src/app

EXPOSE ${_INCAS_SRV_PORT}

ENTRYPOINT ["python3"]

CMD ["-m", "uiuc_incas_server"]
