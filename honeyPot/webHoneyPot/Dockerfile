FROM ubuntu:18.04
ENV PYTHONUNBUFFERED 1 
ADD aliyun_sources.list /etc/apt/sources.list 
RUN apt-get update
RUN apt install python3-pip -y
COPY requirements.txt ./  
RUN pip3 install -r ./requirements.txt
COPY ./webCanary/ ./
RUN cd ./webCanary/
EXPOSE 8000
RUN python3 manage.py migrate
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
