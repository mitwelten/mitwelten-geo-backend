import os 
import psycopg2
import csv
from ..lib import ogr2ogr

cwd = os.path.dirname(os.path.realpath(__file__))
secure_path = os.path.dirname(os.path.dirname(cwd))
connection_string = open(os.path.join(secure_path, "secure/connection_string.txt")).read()
bird_path = os.path.join(cwd, "sample-birdnet.tsv")
location_path = os.path.join(cwd, "sample-location.csv")

#accessors
def getPostGISVersion(cur):
    """Retrieve PostGIS full version information from a pyscopg2 connection cursor

    :param cur: PostGIS database cursor
    :type cur: psycopg2.extensions.cursor

    :return: PostGIS version information list
    :rtype: list
    """
    cur.execute("SELECT PostGIS_Full_Version();")
    return cur.fetchall()

def getGSTables(cur):
    """Retrieve PostGIS full version information from a pyscopg2 connection cursor

    :param cur: PostGIS database cursor
    :type cur: psycopg2.extensions.cursor

    :return: PostGIS version information list
    :rtype: list
    """
    cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'gs%'")
    return cur.fetchall()

#modifiers
def setupTables(cur):
    audiomoths_table = "CREATE TABLE audiomoths (identifier INT PRIMARY KEY, location geography(POINT,4326), name VARCHAR(64));"
    cur.execute(audiomoths_table)

def removeTables(cur):
    audiomoths_table = "DROP TABLE audiomoths;"
    cur.execute(audiomoths_table)

def insertLocationData(cur, file_path):
    sql_template = "INSERT INTO audiomoths (identifier, location, name) VALUES (%s, %s, %s);"
    pg_point = "SRID=4326;POINT(%s %s)"
    with open(file_path) as data:
        datareader = csv.DictReader(data)
        for row in datareader:
            cur.execute(sql_template,
                        (row["Id"], pg_point % (row["Longitude"], row["Latitude"]),row["Name"]))

def insertBirdNetData(cur, file_path, location_id, timestamp):
    with open(file_path) as data:
        datareader = csv.DictReader(data, delimiter="\t")
        for row in datareader:
            print(row)

if __name__ == "__main__":
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    print("There are %i GeoServer tables.\n" % (len(getGSTables(cur))))
    

    #setupTables(cur)
    #insertBirdNetData(bird_path, location_id, timestamp):
    #insertLocationData(cur, location_path)
    #removeTables(cur)

