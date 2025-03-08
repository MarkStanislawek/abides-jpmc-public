# Environmental compatibility as of February 2025

## install github authentication client
```
sudo apt update && sudo apt install -y gh
```

## install dependencies for pyenv(because pyenv compiles python from the source)
```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
```
## install pyenv
```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```
## bashrc updates
```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
```
## onto dev setup
```
pyenv install 3.8
```
### python version selection
```
user@w-mstani9-m7rxo052:~/repos$ cd abides-jpmc-public/
user@w-mstani9-m7rxo052:~/repos/abides-jpmc-public$ pyenv local 3.8
user@w-mstani9-m7rxo052:~/repos/abides-jpmc-public$ which python
/home/user/.pyenv/shims/python
user@w-mstani9-m7rxo052:~/repos/abides-jpmc-public$ python -V
Python 3.8.20
user@w-mstani9-m7rxo052:~/repos/abides-jpmc-public$ python -m venv abides_venv
```

### errors during simulation
Error:
No module found termcolor
```
(abides_venv) user@w-mstani9-m7rxo052:~/repos/abides-jpmc-public$ pip install termcolor
```
### downgrade protobuf
Error:
```
If you cannot immediately regenerate your protos, some other possible workarounds are:
 1. Downgrade the protobuf package to 3.20.x or lower.
 2. Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower).
```
```
(abides_venv) user@w-mstani9-m7rxo052:~/repos/abides-jpmc-public$ pip install protobuf==3.20
```

### missing torch libraries
```
pip install torch==1.7
```

### ray dashboard issues
```
pip install ray[rllib]==1.13.0
```

### tensorboard
Install tensorflow in a separate venv for tensorboard usage.