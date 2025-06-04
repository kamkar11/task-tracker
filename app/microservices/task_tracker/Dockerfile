FROM base-python:3.12.5

WORKDIR /app

COPY *.py /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--log-level", "warning", "main:app"]