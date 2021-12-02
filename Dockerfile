FROM python:latest

ENV HOME /root
ENV PYTHONBUFFERED=1
WORKDIR /root

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python3 app.py