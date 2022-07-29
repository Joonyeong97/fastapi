FROM python:3.10.5

WORKDIR /src

COPY src/* /src/

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
