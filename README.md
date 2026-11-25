# telemetry

Collects system telemetry and stores it in **MySQL** (and can send it over HTTP).

## What is collected

- CPU: physical/logical cores, times, load
- Memory and swap
- Disks: partitions, usage, I/O counters
- Network: bytes/packets, interfaces, link status
- OS information

## Stack

Python 3, `psutil`, `mysql-connector-python`, Pipenv.

## Run

1. Edit `config.py` — MySQL host, user, password, database.
2. Install dependencies and start:

```bash
pipenv install
pipenv run python telemetry.py
```
