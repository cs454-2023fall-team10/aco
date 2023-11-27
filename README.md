# aco

## 0. Prerequisite
``` bash
python3 -m pip install pipenv
```

## 1. Install
``` bash
pipenv shell
pipenv install
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
