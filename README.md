# TrianglePeople

Simulate a group of people where each individual tries to form an equilateral triangle with two random partners from the group without further communication.
Created for fun and to examine wether a large group of perfectionists can ever finish this game.

# Installation

virtualenv for Python is strongly recommended. Only one dependency, `pygame`:

```
pip install pygame
```

# Controls

- `BACKSPACE` : Restart simulation
- `ARROW_UP/ARROW_DOWN` : Increase/decrease number of people involved
- `ARROW_LEFT/ARROW_RIGHT` : Decrease/increase tolerance for triangles formed

# Usage

```
python main.py --help
```

```
usage: main.py [-h] [-s SEED] [-e ERR_TOL] num_people

positional arguments:
  num_people            Number of people to involve. Default is 5

optional arguments:
  -h, --help            show this help message and exit
  -s SEED, --seed SEED  Random seed to use
  -e ERR_TOL, --err_tol ERR_TOL
                        Error tolerance. Default is 5
```
