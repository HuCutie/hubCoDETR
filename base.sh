apt update
apt install -y sudo git vim libgl1-mesa-glx libglib2.0-0 ntp wget tmux
pip install -U openmim
mim install mmcv-full==1.5.0

python setup.py install
pip install -r requirements.txt

pip install matplotlib
pip install fairscale
pip install scipy
pip install timm
pip install yapf==0.40.1