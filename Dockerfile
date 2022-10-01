FROM ghcr.io/illallangi/telegraf:v0.0.9
ENV INFLUXDB_DATABASE=gazelle

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY telegraf.conf /etc/telegraf/telegraf.conf

COPY . /usr/src/app/

