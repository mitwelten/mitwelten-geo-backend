import logging
import sys
import argparse
import pathlib
import os 
import psycopg2
import tempfile
from lib import ogr2ogr
from geoserver.catalog import Catalog

log = logging.getLogger("ogr2ps2gs")
log.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


def existTable(cur, table_name):
    """Check to see if a table 

    :param cur: PostGIS database cursor
    :type cur: psycopg2.extensions.cursor
    :param cur: PostGIS database table name
    :type cur: str

    :return: If the table already exists in the database
    :rtype: bool
    """

    cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", (table_name,))

    return cur.fetchone()[0]

def dropTable(cur, table_name):
    """Check to see if a table 

    :param cur: PostGIS database cursor
    :type cur: psycopg2.extensions.cursor
    :param cur: PostGIS database table name
    :type cur: str

    :rtype: None
    """

    log.warning("The following command is susceptible to SQL injection.")

    #psycopg2 does not correctly/safely mogrify the following command
    #consider using a regular expression to check for safety
    #sql = cur.mogrify("DROP TABLE IF EXISTS %s", (table_name,))

    sql = "DROP TABLE IF EXISTS \"%s\"" % table_name

    log.debug("Sending SQL: %s" % sql)
    cur.execute(sql)

def insertVector(cur, in_path,table_name):
    log.info("Attempting to create table %s from %s" % (table_name, in_path))
    
    log.debug("Checking if table %s already exists" % table_name)
    if existTable(cur, table_name):
        log.error("Table %s already exists" % table_name)
        raise psycopg2.errors.DuplicateTable("%s table already exists" % table_name)

    log.debug("Converting file %s to PostgreSQL" % in_path)
    tmp = tempfile.NamedTemporaryFile()
    try:
        ogr2ogr.main(["","-f", "PGDump", tmp.name, in_path, "-a_srs", "EPSG:4326", "-nln", table_name, "-lco", "GEOM_TYPE=geography"])
    except RuntimeError as e:
        log.error("GDAL failed to convert %s" % in_path)
        raise e

    log.debug("Attempting to create table %s" % table_name)
    cur.execute(tmp.read())

    if existTable(cur, table_name):
        log.debug("Table %s created" % table_name)
    else:
        log.error("Could not create table %s" % table_name)
        raise psycopg2.errors.ConnectionException("Table %" % table_name)


def publishVector(cur, table_name, geoserver_user):
    log.debug("Adding table read premisison to user %s" % geoserver_user)
    try:
        cur.execute("GRANT SELECT ON TABLE %s TO geoserver" % (table_name))
    except psycopg2.errors.UndefinedTable as e:
        log.error("Table %s does not exist" % table_name)
        raise e


parser = argparse.ArgumentParser(description="Store vector data from a file in a PostGIS database and publish it to GeoServer")
parser.add_argument("-v", "--version", help="show program version", action="store_true")
parser.add_argument("-l", "--log", help="Log activity to the specified file", action="store_true")
parser.add_argument("-dt", "--droptable", help="Drop table if it already exists", action="store_true")
parser.add_argument("name", help="The table name to use for the vector data in PostGIS", type=str)
parser.add_argument("path", help="Vector data to store in PostGIS and publish to GeoServer", type=pathlib.Path)

if __name__ == "__main__":
    args = parser.parse_args()

    in_path = os.path.abspath(str(args.path))
    table_name = args.name
    
    if args.version:
        log.info("Version number 0.0.0")
        
    try:
        log.debug("Loading default credentials")
        cwd = os.path.dirname(os.path.realpath(__file__))
        secure_path = os.path.join(os.path.dirname(cwd), "secure")
        pyscopg2_connection_string = open(os.path.join(secure_path, "private_psycopg2_connection_string.txt")).read()
        gsconfig_url = open(os.path.join(secure_path, "private_gsconfig_url.txt")).read()
        gsconfig_username = open(os.path.join(secure_path, "private_gsconfig_username.txt")).read()
        gsconfig_password = open(os.path.join(secure_path, "private_gsconfig_key.txt")).read()

    except FileNotFoundError as e:
        log.error("Missing default credentials")
        log.error(str(e))


    log.info("Connecting to database")        
    conn = psycopg2.connect(pyscopg2_connection_string)
    conn.autocommit = True
    cur = conn.cursor()
    #cur.execute("DROP TABLE IF EXISTS \"gs_extent\"")

    if args.droptable:
        log.info("Dropping table %s if it exists" % table_name)
        dropTable(cur, table_name)
##        cur.close()
##        conn.commit()
##        conn.close()
##
##        log.debug("Reopening connection to database")
##        conn = psycopg2.connect(pyscopg2_connection_string)
##        cur = conn.cursor()

    insertVector(cur, in_path, table_name)


    log.debug("Commiting changes to database and closing connection")
    conn.commit()
    conn.close()

