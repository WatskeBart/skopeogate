FROM registry.access.redhat.com/ubi9/python-312-minimal:latest

ARG BUILD_MODE=offline

USER 0

WORKDIR /opt/app-root/src

COPY . .

RUN sh ./builder.sh && \
    rm ./builder.sh

# Geen bytecode caching (__pycache__) en geen stdout buffering, zodat logs direct zichtbaar zijn
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000/tcp
USER 1001

CMD ["fastapi", "run", "main.py"]
