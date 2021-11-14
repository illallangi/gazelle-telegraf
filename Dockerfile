FROM docker.io/library/python:3.8.5

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    XDG_CONFIG_HOME=/config

RUN curl -s https://repos.influxdata.com/influxdb.key | apt-key add -
RUN echo "deb https://repos.influxdata.com/debian buster stable" > /etc/apt/sources.list.d/influxdb.list
RUN apt-get update && \
    apt-get install -y --no-install-recommends telegraf iputils-ping snmp procps lm-sensors && \
    rm -rf /var/lib/apt/lists/*

ADD entrypoint.sh /entrypoint.sh
ADD telegraf.conf /etc/telegraf/telegraf.conf

WORKDIR /usr/src/app
ADD . /usr/src/app

RUN pip3 install .

ENTRYPOINT ["/entrypoint.sh"]
RUN chmod +x /entrypoint.sh
CMD ["telegraf"]

ARG VCS_REF
ARG VERSION
ARG BUILD_DATE
LABEL maintainer="Andrew Cole <andrew.cole@illallangi.com>" \
      org.label-schema.build-date=${BUILD_DATE} \
      org.label-schema.description="TODO: SET DESCRIPTION" \
      org.label-schema.name="GazelleTelegraf" \
      org.label-schema.schema-version="1.0" \
      org.label-schema.url="http://github.com/illallangi/GazelleTelegraf" \
      org.label-schema.usage="https://github.com/illallangi/GazelleTelegraf/blob/master/README.md" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/illallangi/GazelleTelegraf" \
      org.label-schema.vendor="Illallangi Enterprises" \
      org.label-schema.version=$VERSION
