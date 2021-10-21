FROM python:3.8

WORKDIR /main
COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["main.py"]