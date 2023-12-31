ARG BASE_IMAGE_TAG=latest
FROM ghcr.io/korkin25/slotegrator-task3-base-image:${BASE_IMAGE_TAG}

WORKDIR /app
RUN mkdir logs
RUN mkdir config
RUN mkdir templates

COPY app.py .
COPY config.yaml config/
COPY headers.html templates/

EXPOSE 5000

CMD ["python", "app.py", "config/config.yaml"]
