FROM ghcr.io/illallangi/telegraf:v0.0.6
ENV INFLUXDB_DATABASE=gazelle


RUN \
  DEBIAN_FRONTEND=noninteractive \
  apt-get update \
  && \
  apt-get install -y --no-install-recommends \
    postgresql-common=200+deb10u5 \
  && \
  rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY telegraf.conf /etc/telegraf/telegraf.conf

COPY . /usr/src/app/

