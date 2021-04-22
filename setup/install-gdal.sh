sudo apt-get install build-essential autoconf automake libtool curl make g++ unzip
sudo apt install libspatialindex-dev
sudo apt-get install proj-bin python2-dev python3-dev
sudo pip3 install numpy
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
sudo ldconfig

sudo apt-get install libsqlite3-dev libtiff5-dev libcurl4-openssl-dev

#reboot?

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
./configure --prefix=g/usr/local/gdal/gdal-3.2.2 --with-python
make
sudo make install
sudo pip3 install gdal-3.2.2/swig/python
