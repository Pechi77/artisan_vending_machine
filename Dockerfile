
FROM python:3.9

WORKDIR /artisan_vending_machine

COPY . /artisan_vending_machine

RUN pip install -r requirements.txt

EXPOSE 8000

ENV USERNAME admin
ENV PASSWORD admin
ENV MYSQL_HOST localhost
ENV DATABASE artisan

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
