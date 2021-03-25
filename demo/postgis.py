import os 
import psycopg2
import csv

cwd = os.path.dirname(os.path.realpath(__file__))
secure_path = os.path.dirname(os.path.dirname(cwd))
connection_string = open(os.path.join(secure_path, "secure/connection_string.txt")).read()
bird_path = os.path.join(cwd, "sample-birdnet.tsv")
location_path = os.path.join(cwd, "sample-location.csv")

def getPostGISVersion(cur):
    cur.execute("SELECT PostGIS_Full_Version();")
    return cur.fetchall()

def setupTables(cur):
    audiomoths_table = "CREATE TABLE audiomoths (identifier INT PRIMARY KEY, location geography(POINT,4326), name VARCHAR(64));"
    cur.execute(audiomoths_table)

def removeTables(cur):
    audiomoths_table = "DROP TABLE audiomoths;"
    cur.execute(audiomoths_table)

def insertLocationData(cur, file_path):
    sql_template = "INSERT INTO audiomoths VALUES (%s, %s, %s);"
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

    setupTables(cur)
    #insertBirdNetData(bird_path, location_id, timestamp):
    insertLocationData(cur, location_path)
    #removeTables(cur)

