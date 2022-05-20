FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
ENV PYTHONPATH "${PYTHONPATH}:/code/app"
ENV PYTHONUNBUFFERED 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
