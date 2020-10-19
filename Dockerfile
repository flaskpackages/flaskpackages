FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install flask; python setup.py install

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "flask_packages.web:app"]
