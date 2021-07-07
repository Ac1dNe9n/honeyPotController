FROM ubuntu:18.04
ENV PYTHONUNBUFFERED 1 
ADD aliyun_sources.list /etc/apt/sources.list 
RUN apt-get update
RUN apt install python3-pip -y
COPY requirements.txt ./  
RUN pip3 install -r ./requirements.txt
COPY mysqlHoneyPot.py ./
EXPOSE 3306
CMD ["python3", "mysqlHoneyPot.py"]
