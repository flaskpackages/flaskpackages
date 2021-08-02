ARG PYTHON_VERSION=3.8

FROM python:${PYTHON_VERSION}

COPY . /app
WORKDIR /app

RUN pip install flask; python setup.py install

EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--config", "gunicorn_config.py", "flask_packages.web:app"]