import os 
import psycopg2
import csv
import tempfile

#os.environ["GDAL_LIBRARY_PATH"] =  "/usr/local/gdal/gdal-3.2.2/lib/libgdal.so"

from lib import ogr2ogr

#database connetion strings
cwd = os.path.dirname(os.path.realpath(__file__))
secure_path = os.path.join(os.path.dirname(cwd), "secure")
pyscopg2_connection_string = open(os.path.join(secure_path, "psycopg2_connection_string_private.txt")).read()

#sample data paths
bird_path = os.path.join(cwd, "data/sample-birdnet.tsv")
location_path = os.path.join(cwd, "data/sample-location.csv")
extent_path = os.path.join(cwd, "data/extent.kml")

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


def insertVector(cur, in_path,table_name):
    #check if table name exists already
    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = %s", (table_name,))
    if cur.fetchone() == 1:
        raise psycopg2.errors.DuplicateTable("%s table already exists" % table_name)
    else:
        print("Attempting to create table %s" % table_name)

    #convert to SQL
    tmp = tempfile.NamedTemporaryFile()
    try:
        ogr2ogr.main(["","-f", "PGDump", tmp.name, in_path, "-a_srs", "EPSG:4326", "-nln", table_name, "-lco", "GEOM_TYPE=geography"])
    except (RuntimeError):
        raise psycopg2.errors.ConnectionException("GDAL appears to have failed to convert table %s" % in_path)

    #create table
    cur.execute(tmp.read())

    #add read permissions for geoserver group
    try:
        cur.execute("GRANT SELECT ON TABLE %s TO geoserver" % (table_name))
    except (psycopg2.errors.UndefinedTable):
        pass
        
    
if __name__ == "__main__":
    conn = psycopg2.connect(pyscopg2_connection_string)
    cur = conn.cursor()


    print("There are %i GeoServer tables." % (len(getGSTables(cur))))

    insertVector(cur, extent_path,"gs_extent")
    
    print("There are %i GeoServer tables." % (len(getGSTables(cur))))

    
    #setupTables(cur)
    #insertBirdNetData(bird_path, location_id, timestamp):
    #insertLocationData(cur, location_path)
    #removeTables(cur)

