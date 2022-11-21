conda init zsh
conda init bash 
eval "$(conda shell.bash hook)"
# conda update -n base -c defaults conda
conda create --name diffusers python=3.9 -y
conda activate diffusers
pip install git+https://github.com/ShivamShrirao/diffusers.git
pip install -U -r requirements.txt
pip install pyheif
pip install piexif
pip install bitsandbytes
pip install aiofiles
pip install python-multipart
# pip install celery==4.4.1 Flask==2.1.0 redis==3.4.1
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
rm redis-stable.tar.gz
cd redis-stable
make
sudo make install
# redis-server
