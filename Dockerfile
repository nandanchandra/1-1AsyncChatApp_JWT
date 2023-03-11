FROM python:alpine3.17 as base

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc  libc-dev  linux-headers \
    postgresql-dev 

# Install dependencies
COPY requirements.txt /app/requirements.txt 
RUN pip install -r /app/requirements.txt

# Now multistage build
FROM python:alpine3.17
RUN apk add libpq
COPY --from=base /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

# Set work directory
WORKDIR /app
# Copy project
COPY . /app

ENV PYTHONUNBUFFERED 1