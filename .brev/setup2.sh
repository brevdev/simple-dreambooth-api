conda init zsh
conda init bash 
eval "$(conda shell.bash hook)"
# conda update -n base -c defaults conda
conda create --name diffusers2 python=3.9 -y
conda activate diffusers2
pip install git+https://github.com/ShivamShrirao/diffusers.git
pip install -U -r requirements.txt
