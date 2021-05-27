# REST API for Postgresql

Setup explained [here](https://postgrest.org/en/v7.0.0/tutorials/tut0.html)

## Installation

Postgresql C-library
```sh
sudo apt-get install libpq-dev
```
Download PostgREST
```sh
wget https://github.com/PostgREST/postgrest/releases/download/v7.0.1/postgrest-v7.0.1-linux-x64-static.tar.xz

tar xJf postgrest-v7.0.1-linux-x64-static.tar.xz
```

## Configuration

Configuration is done in a .config file:

```conf
db-uri = "postgres://authenticator:password@localhost:5432/resttest"
#                    ^--- role       ^--- password                  ^--- database name          
db-schema = "api"
db-anon-role = "web_anon"
```

PostgREST runs by default on port 3000.

## Usage

**Start PostgREST**
```sh
./postgrest my_config_file.conf
```

Or use a [systemd service](postgrest.service)

Example table `location`

name|type
-|-
location_id|integer
latitude|float
longitude|float
name|text

**GET**

More information [here](https://postgrest.org/en/stable/api.html#tables-and-views)

```sh
# get all elements
curl http://localhost:3000/<table_name>

# filter by id 
curl http://localhost:3000/location?location_id=eq.100

# get all location with longitude less than 8.5
curl http://localhost:3000/location?longitude=lt.8.5
```

**POST**
```sh
# add a new location with id 10001
curl http://localhost:3000/location -X POST \
     -H "Content-Type: application/json" \
     -d '{"location_id": 10001, "latitude":47.53891207153036,"longitude": 7.613804923629768}'
```