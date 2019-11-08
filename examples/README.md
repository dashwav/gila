# Examples of gila usage

All of these examples are built such that the user can ''drag and drop'' code into their projects. All of the provided scripts work as is, and detail various scenarios of project design. These all assume you have gila installed into the system. 

### Principles
Two of the main principles for gila is the idea of a singleton\* instance and hierarchical loading. These terms will be referenced and are at the core of how gila operates.
* A singleton instance: Only holds a single instantiation of an object which once originally instantiated, always has the same pointers.
* Hierarchical loading: Operating under the pretense that some configurations overshadow others.
    * Specifically in our case `alises > overrides > environment > config > defaults` where things are shadowed from left to right.

### First Look
The most basic use case of gila is layed out on `simple-example/` which showcases the common usecases: default values, reading from the environment, and retrieving values. It makes use of the file `config.yml` in the same directory. It is suggested to start here before diving into the other examples.

### Further examples are explored in the subdirectories.

The structure of them are as follows:
```
examples/
| README.md  # The file you are reading
| simple-example.py  # Simple use case
|
|____subdir/  # subdirectory of common use cases
|    | README.md  # Detail explanation of the code
|    | example.py  # the example use case
|    | config.yml  # (Optional) Additional configuration parameters to read in
|    | misc.py  # (Optional) Additional functions that are read into the example.
...
```

### To Run:
All of the following code provided follows a similar calling structure of:
```
python example.py
```
In some cases command line arguments can be used and it is suggested to read each subdirectories respective `README.md`

#### Cloning the repo without installing gila
If you do not have gila installed onto the system (assuming you just ran `git clone`) the files will not work ''out of the box'', but rather you should add this bit of code to the top of the example you want to run (just above `import gila`).
```python
import os
import sys
cwd = os.getcwd()
sys.path.insert(1, '/'.join(cwd.split('/')[:-2]))
```
This code prepends the gila root directory to your system path such that a relative import of gila can be done.
