ARG PYTHON_VERSION=3.8

FROM python:${PYTHON_VERSION}

COPY . /app
WORKDIR /app
RUN chmod +x /app/entrypoint.sh

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--config", "gunicorn_config.py", "flask_packages.web:app"]