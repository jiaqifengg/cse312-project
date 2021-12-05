FROM python:3.10

ENV HOME /root
WORKDIR /root

EXPOSE 5000
COPY . .
RUN pip install -r requirements.txt
RUN FLASK_APP==app.py
RUN FLASK_ENV==development


ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

CMD /wait && python app.py