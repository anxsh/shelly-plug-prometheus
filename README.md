# shelly-plug-prometheus

Simple web server that exports Prometheus metrics for the Shelly Plug US.

# Installation

Create a credentials YAML file with two fields `user` and `pass` containing credentials for the Shelly API. Put it at `/etc/shelly-credentials.yml`

```
sudo cp shelly-plug-prometheus-server.py /usr/local/bin
sudo cp shelly-plug-prometheus-server.service /etc/systemd/system/
sudo systemctl start shelly-plug-prometheus-server.service
sudo systemctl enable shelly-plug-prometheus-server.service
```
