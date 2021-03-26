sudo apt install nvidia-cuda-dev nvidia-cuda-toolkit nvidia-driver

wget https://developer.download.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/9.2_20191031/Ubuntu16_04-x64/libcudnn7-dev_7.6.5.32-1%2Bcuda9.2_amd64.deb
sudo dpkg -i libcudnn7-dev_7.6.5.32-1+cuda9.2_amd64.deb 
sudo apt-get install -f

sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6

wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
bash Anaconda3-2020.11-Linux-x86_64.sh
conda config --set auto_activate_base false

conda create -n tf-gpu-cuda8 tensorflow-gpu cudatoolkit=9.0
conda activate tf-gpu-cuda8

sudo apt-get install git
git clone https://github.com/kahst/BirdNET.git
cd BirdNET
pip3 install -r requirements.txt
sh model/fetch_model.sh

sudo apt-get install ffmpeg

pip install -r https://raw.githubusercontent.com/Lasagne/Lasagne/master/requirements.txt
pip install https://github.com/Lasagne/Lasagne/archive/master.zip

sudo apt-get install libblas-dev liblapack-dev

sudo apt-get install cmake
pip3 install Cython 

sudo apt-get install libbsd-dev pkg-config
cd ..
git clone https://github.com/Theano/libgpuarray.git
cd libgpuarray
mkdir Build
cd Build
cmake .. -DCMAKE_BUILD_TYPE=Release
make
sudo make install
cd ..
python3 setup.py build
python3 setup.py install
sudo ldconfig






