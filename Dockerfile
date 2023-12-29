FROM ghcr.io/slotegrator-task3-base-image:latest

WORKDIR /app
RUN mkdir logs
RUN mkdir config
RUN mkdir templates

COPY app.py .
COPY config.yaml config/
COPY headers.yaml templates/

EXPOSE 5000

CMD ["python", "app.py", "config/config.yaml"]
