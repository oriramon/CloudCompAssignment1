FROM python:alpine3.17
WORKDIR ./app
RUN pip install flask
RUN pip install flask_restful
RUN pip install requests
COPY rest-meal-svr-v1.py .
EXPOSE 8000
ENV FLASK_APP=rest-meal-svr-v1.py
ENV FLASK_RUN_PORT=8000
CMD ["flask", "run", "--host=0.0.0.0"]