FROM ubuntu:latest


RUN apt update && apt install  openssh-server sudo python3 libgl1-mesa-dev -y
RUN apt install -y git bash 

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip




WORKDIR /
COPY start.sh /start.sh
RUN chmod 755 /start.sh

RUN mkdir /opt/app
COPY . /opt/app/

RUN pip3 install -r /opt/app/requirements.txt

EXPOSE 8000

CMD ["/start.sh"]