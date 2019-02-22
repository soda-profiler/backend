FROM python:3.6
RUN apt update 
ADD ./requirements.txt /
RUN pip install -r requirements.txt
ADD ./soda /code
WORKDIR /code
EXPOSE 80
CMD ["gunicorn", "gncrn:app", "--bind", "0.0.0.0:80", "--worker-class", "sanic.worker.GunicornWorker"]