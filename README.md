# Signified Playtesting

This repository is an intermediate form between a paper prototype and Unity software.
The idea is to allow technical game developers to quickly prototype and iterate upon design.
We are working on Signified: a deckbuilder roguelike autobattler card game.

The envisioned experience of using this repo is creating paper cards and enemies.
While running combat, you can keep track of damage / stats using commands in the Jupyter notebook.
The notebook also simulates the shop and keeps track of your current roster.

## Getting started

1. Set up a virtual environment.
```{bash}
python -m venv .venv
source .venv/bin/activate
```
2. Install the requirements.
```{bash}
pip install -r requirements.txt
```
3. Run the Jupyter server and open the playground Notebook.
```{bash}
jupyter lab
```
