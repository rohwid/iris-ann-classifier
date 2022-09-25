FROM python:3.8-slim-buster as base

FROM base as builder 

COPY ./requirements.txt ./scripts/install.sh ./
RUN ./install.sh && python -m venv /opt/venv

# setup venv as path
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
RUN pip install gunicorn

FROM base

RUN apt-get update \
    && apt-get -y install procps

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /opt/apps/project

# Main API
CMD ["gunicorn", "-w", "1", "-t", "600", "-b", "0.0.0.0:8080", "endpoint:app", "-n", "iris-ann"]
