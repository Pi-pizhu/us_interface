FROM python:3

RUN apt-get update \
    && apt-get install git-core \
    && mkdir /opt/api-test
    && cd /opt/api-test
    && git clone git@github.com:Pi-pizhu/us_interface.git
    && pip3 install -r us_interface/requirements.txt
WORKDIR /opt/api-test/us_interface