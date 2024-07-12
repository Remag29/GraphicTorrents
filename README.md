# Graphic-Torrents

Graphic-Torrent is a project that aims to create a nice layout to display your torrents and their "Score".

The goal is to help you to identify the best torrents in a quick way. The "Score Torrent" is calculated based on the size of the file, the volume of uploads and the number of active days.

For now, it **only works with qBittorrent**.

## Score Torrent
Formulas:

```
sc = (U/S) / T
```

Where:

- sc is the score of the torrent
- U is the volume of uploads
- S is the size of the file
- T is the number of active days

In a nutshell, higher is the upload volume in a short period of time, higher is the score.

## How to use

### Docker
You can use the project with the following docker image:

```
remag297/graphic-torrent:latest
```

A docker-compose file is available in the repository to help you to start the project.

```yaml
---
services:
  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - WEBUI_PORT=8080
      - TORRENTING_PORT=6881
    volumes:
      - ./tests/qbittorrent/config:/config
      - ./tests/qbittorrent/downloads:/downloads
    ports:
      - 8080:8080
      - 6881:6881
      - 6881:6881/udp
    restart: unless-stopped

  graphic-torrent:
    image: graphic-torrent:latest
    container_name: graphic-torrent
    build:
        context: .
        dockerfile: Dockerfile
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - QB_URL=${QB_URL}
      - QB_USERNAME=${QB_USERNAME}
      - QB_PASSWORD=${QB_PASSWORD}
#      - FLASK_ENV=development
#      - FLASK_DEBUG=1
    ports:
      - 5000:5000
    depends_on:
      - qbittorrent
    restart: no
```
### .env file

You need to create a `.env` file in the root of the project with the following variables:

```shell
QB_URL=http://qbittorrent:8080
QB_USERNAME=admin
QB_PASSWORD=changeme
```
