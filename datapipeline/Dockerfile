FROM python:3.8-slim

WORKDIR datapipeline

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD python -m uvicorn app:app --reload --host 0.0.0.0 --port 8080