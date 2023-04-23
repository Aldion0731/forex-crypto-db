## FOREX-CRYPTO-DB

The project is a Python application that uses the [yfinance](https://pypi.org/project/yfinance/) module to download historical data for currencies and cryptocurrencies and stores the results in a [PostgreSQL](https://www.postgresql.org/) database. The database runs in a [Docker](https://www.docker.com/) container that contains an updater script that periodically downloads data and uploads to the database.

___

### Pre-requisites
To use this project, you need the following:

`Python 3.10`
`pipenv`
`Docker`
___
### Installation

Clone this repository to your local machine.

```bash
git clone git@github.com:Aldion0731/forex-crypto-db.git
```
Install dependencies

```bash
pipenv sync
```

### Database configurations

- Copy ane rename the `.env.template` file to `.env`
- Modify the values to our own secret values.
    - Currently the migration scripts and updater are not running inside the converter so the db port is exposed. This will be modified ina future version.
___

### Usage
##### Running the docker container

```bash
docker-compose up
```

##### Run Migration Scripts

```bash
alembic upgrade heads
```

### Update the database

```bash
python -m src.scripts.updater
```

