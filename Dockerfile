FROM python:3

RUN apt-get update -y \
    && apt-get install -y python3-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./shelly-plug-prometheus-server.py", "--shelly_address", "shelly-plug-1" ]
