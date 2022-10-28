conda init zsh
conda init bash 
eval "$(conda shell.bash hook)"
# conda update -n base -c defaults conda
conda create --name diffusers python=3.9 -y
conda activate diffusers

# pip install . # TODO: maybe we don't need this
# pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116 # TODO: maybe we don't need this 
pip install -r requirements.txt
pip install -U --pre triton # TODO: this wasn't found - maybe to do with prior install steps
pip install ninja bitsandbytes



# mkdir ~/github
# cd ~/github
# git clone https://github.com/ShivamShrirao/diffusers.git
# cd diffusers
# sudo apt-get install git-lfs


# TODO: checkout how long this'd take:
# pip install git+https://github.com/facebookresearch/xformers@1d31a3a#egg=xformers