FROM python:3.11-alpine AS builder

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/app

COPY requirements.txt requirements.txt

RUN apk --no-cache add python3-dev musl-dev gcc curl && \
    python -m venv /usr/app/venv

RUN mkdir -p /usr/app/shared-libs && \
    curl -sS https://installers.intelligentvoice.com/iv-artifacts/iv-libs-gearman-trunk.tar | tar x -C /usr/app/shared-libs && \
    rm -f iv-libs-gearman-trunk.tar && \
    pip install --quiet --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --quiet --no-cache-dir /usr/app/shared-libs/iv-libs-gearman/python-dependencies/python3_gmtasks-*.whl && \
    pip install --quiet --no-cache-dir --upgrade -r /usr/app/shared-libs/iv-libs-gearman/requirements.txt && \
    rm -rf /usr/app/shared-libs/iv-libs-gearman/python-dependencies/python3_gmtasks-*.whl && \
    rm -rf /usr/app/shared-libs/iv-libs-gearman/requirements.txt && \
    pip install --quiet --no-cache-dir --upgrade -r requirements.txt && \
    rm -rf requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/usr/app/shared-libs/iv-libs-gearman"

COPY . .

CMD ["python", "./test_riw.py"]
