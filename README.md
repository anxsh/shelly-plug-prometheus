# shelly-plug-prometheus

Simple web server that exports Prometheus metrics for the Shelly Plug US.

# Build

```
docker build -t shelly-plug-prometheus .
```

# Run

```
docker run -it -p PORT:PORT --add-host=HOST:IP --rm --name shelly-plug-prometheus shelly-plug-prometheus:latest
```
