FROM python:3.7-stretch

RUN pip install pymongo flask flask-cors

RUN mkdir /rest-search
WORKDIR /rest-search

COPY indexdao indexdao
COPY pagedetailsdao pagedetailsdao
COPY PageDetails.py PageDetails.py
COPY app.py app.py

COPY main.py main.py

ENV MONGODB_HOST mongo
ENV MONGODB_PORT 27017
ENV MONGODB_DB default
ENV MONGODB_ORTSINDEX_COLLECTION locationindex
ENV MONGODB_ZEITINDEX_COLLECTION timeindex
ENV MONGODB_PAGEDETAILS_COLLECTION pagedetails
ENV MONGODB_WORDINDEX_COLLECTION wordindex

ENV MONGODB_USERNAME genericparser
ENV MONGODB_PASSWORD genericparser

ENV FLASK_HOST 0.0.0.0
ENV FLASK_PORT 8181

ENV DEBUG true

CMD ["python3", "-u", "main.py"]
