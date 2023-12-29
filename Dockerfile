FROM ghcr.io/slotegrator-task3-base-image:latest

WORKDIR /app
RUN mkdir -p logs
RUN mkdir -p templates

COPY app.py .
COPY config.yaml .
COPY headers.yaml .

EXPOSE 5000

CMD ["python", "app.py", "config.yaml"]
