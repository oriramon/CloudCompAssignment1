FROM python:alpine3.17
WORKDIR ./app
RUN pip install flask
RUN pip install flask_restful
RUN pip install requests
COPY rest-word-svr-v1.py .
EXPOSE 7000
ENV FLASK_APP=rest-word-svr-v1.py
ENV FLASK_RUN_PORT=7000
CMD ["flask", "run", "--host=0.0.0.0"]