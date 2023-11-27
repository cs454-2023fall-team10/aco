# aco

## 0. Prerequisite
Choose virtual environment, pipenv or conda
``` bash
### Using pipenv
python3 -m pip install pipenv
pipenv shell
pipenv install

### Using conda
conda create -n <env_name> python=3.10.11
conda activate <env_name>
```

## 1. Install
### 1) (Only for conda env) Install module for ACO
``` bash
### Only needed for conda env
pip install -r requirements.txt
```

### 2) Install graphviz
```bash
### For Linux user
sudo apt-get install graphviz

### For macOS user
brew install graphviz
```

### 3) Install submodules
```bash
make init_submodule
```

If you want to re-install submodules (install newer submodule),
``` bash
make clean_submodule
make init_submodule
```

## 2. Run
``` bash
# Run chatbot_graph
python chatbot_graph.py

# Run transformation_graph
python transformation_graph.py

# Run aco
python aco.py
```
