# RayForge
A game engine made with RayLib.

## Getting Started
1) Install Python
2) Open cmd/terminal and type:

```
pip install RayForge
```

## Examples
# Creating a window
``` python
from rayforge import *

forge = RayForge()

@forge.draw
def draw():
    pass

@forge.update
def update():
    pass

forge.run()
```