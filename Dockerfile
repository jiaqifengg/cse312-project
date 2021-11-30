FROM python:3.9.7

ENV HOME /root

WORKDIR /root

COPY . .


RUN pip install -r requirements.txt
RUN pip install flask-mysqldb
RUN pip install bcrypt

EXPOSE 8080

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait

RUN chmod +x /wait

CMD /wait && python app.py