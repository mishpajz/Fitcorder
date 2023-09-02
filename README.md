# Fitcorder

example _docker-compose.yml_
```
version: '3'
services:
  fitcorder:
    image: fitcorder:latest
    ports:
      - $APIPORT:5000
    volumes:
      - $VOLUMEDIR:/app/volume
      - $CONFIGDIR:/app/config
    environment:
      TZ: Europe/Prague
    restart: unless-stopped
```

where:
- `APIPORT` is port for configuration website,
- `VOLUMEDIR` is directory where created video files will be stored
- `CONFIGDIR` is directory containing __cookies.txt__ and where created config files will be stored
