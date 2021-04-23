sudo apt-get install build-essential autoconf automake libtool curl make g++ unzip
sudo apt install libspatialindex-dev postgresql-12
#not sure why python2-dev is required
sudo apt-get install proj-bin python2-dev python3-dev
sudo pip3 install numpy
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
sudo ldconfig

sudo apt-get install libsqlite3-dev libtiff5-dev libcurl4-openssl-dev

#a reboot fixed the finding of some new libraries

wget https://download.osgeo.org/proj/proj-8.0.0.tar.gz
tar -xvf proj-8.0.0.tar.gz
#this is only needed to avoid downloading grids from https://cdn.proj.org
wget https://download.osgeo.org/proj/proj-data-1.5.tar.gz
tar -xvf -C proj-8.0.0/data proj-data-1.5.tar.gz
cd proj-8.0.0
./configure
make
sudo make install
cd ..

wget http://download.osgeo.org/gdal/3.2.2/gdal-3.2.2.tar.gz
tar -xvf gdal-3.2.2.tar.gz
cd gdal-3.2.2
#not sure if better to add --with-curl
#./configure --prefix=/usr/local/gdal/gdal-3.2.2 --with-python --with-pg
./configure --with-python --with-pg
#if necessary first make clean
make
sudo make install
sudo pip3 install gdal-3.2.2/swig/python
#export PATH="/usr/local/gdal/gdal-3.2.2/bin:$PATH"
#confirm postgres support
gdalinfo --formats | grep PostGIS
ogr2ogr --formats | grep PostgreSQL


