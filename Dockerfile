FROM python:3.8-slim-buster

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN apt-get update && apt-get -y install gcc libssl-dev && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python setup.py install

# @TODO Modify api_server to get certificate from files passed as arguments instead of relying on the environment
ENV INCAS_SRV_CERT_PATH="/usr/src/app/certs/uiuc_incas_server_general.crt"
ENV INCAS_SRV_KEY_PATH="/usr/src/app/certs/uiuc_incas_server_general.key"
ARG INCAS_SRV_PORT=8443
ENV INCAS_SRV_PORT=$INCAS_SRV_PORT

# ENTRYPOINT ["python3"]
# CMD ["-m", "uiuc_incas_server"]

WORKDIR /usr/src/app/uiuc_incas_server
CMD ["sh", "-c", "uwsgi --https 0.0.0.0:${INCAS_SRV_PORT},${INCAS_SRV_CERT_PATH},${INCAS_SRV_KEY_PATH} --need-app --master -p 8 -w wsgi:application"]
