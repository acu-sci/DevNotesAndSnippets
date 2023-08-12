# Classic python install

install a .py script to call methods defined in python through command line without having to call python itself
> python setup.py install --user

---
# Package Management Architecture

Package management clients -> (pip/brew/conda)  
### The package management tool:
* specifies dependencies and index locations.  
config(requirements.txt/Pipfile/environment.yml)  

---
# Use of pip + virtualenv
- locate python site packages directory
  >which python  

  e.g. /usr/bin/python

- install virtual environment:
  - go to desired folder and create virtualenv
    for python2
    > virtualenv venv-01

    for python3
    > python -m venv venv-01

- activate virtual environment
  >source venv-01/bin/activate  

  or in windows
  >.\venv-01\Scripts\activate  


- install packages in activated venv with pip

-----------in vs code---------------
Control+Shift+P
Python: Select interpreter
enter path> look for .\venv-01\Scripts\python.exe

----------------------- pipenv ----------------------------------
-------*Easy start:
install the first package needed:
pipenv install pandas
-> This creates a virtual environment and then installs pandas in it
-> after venv is created have to run the shell to go into the venv
pipenv shell

-------*Full start:
The project should have a Pipfile which describes the package dependencies
example of pipfile:
###################
# Pipfile is a TOML formatted description of your project runtime and direct dependencies.[[source]]
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
zeep = "*"
pandas = "*"

[requires]
python_version = "3.8"

[scripts] ---> allows the definition of scripts analog to setup.py
soap_api = 'python main.py'
##################

Use of pipenv
Once the corresponding Pipfile is in place
First time do, generating a pipfile.lock
>pipenv install

After changing the script do
>pipenv install --deploy
definition of deploy option:
--deploy — Make sure the packages are properly locked in Pipfile.lock, and abort if the lock file is out-of-date.

Then run the scripts like

>pipenv run SCRIPT_NAME

pipenv guide: https://realpython.com/pipenv-guide/ 
---
# Create Jupyter Notebook
- from pipenv shell
> pipenv install jupyter  
> pipenv run jupyter notebook

- from vs code
> Ctrl+Shift+P  
> Jupyter: Create Blank New Jupyter Notebook
---
# show matplotlib grpahs in vs-code
right click -> run current file in python interactive window -> click over it
---

-------------------------------------------------------------------------------
---------------------- use logging in python ----------------------------------
-------------------------------------------------------------------------------

from .log2db import main
import logging
# define a format to write lines in log
log_format = '%(asctime)s %(levelname)s::%(message)s'
# define the basic configuration of the log
logging.basicConfig(filename='log/log_name_run.log',
                    format=log_format,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

logging.debug('A debug message')
logging.info('Some information')
logging.warning('A shot across the bows')

#output:
#2004-07-02 13:00:08,743 DEBUG A debug message
#2004-07-02 13:00:08,743 INFO Some information
#2004-07-02 13:00:08,743 WARNING A shot across the bows

<br> . 

# Define a class
Useful to have an object with intrinsic functions to call e.e. model.fit()

``` python
class Converter:

    # method to initialize parameters/atributes
    def __init__(
            self,
            config: str,
            input_fodler: str,
            output_folder: str = "./result",
            verbose: bool = False
    ) -> None:
        """__init__ define class

        Args:
            bla
            bla2
            bla3
        """

        # initialize parameters/atributes
        self.config = config
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.verbose = verbose
```

<br>

# List comprehension
create a list from a for loop with a filter in one step
``` python
files = [
    os.path.join(source_folder, file)
    for file in os.listdir(source_folder)
    if os.path.isfile(os.path.join(source_folder, file)) and re.match(filemask, file)
]
```

<br>  

# Pass an exception message
``` python
try:
    do_stuff()
except Exception:
    print(traceback.format_expection())
```
or
``` python
import sys

try:
    f = open('myfile.txt')
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
```

<br>  

# Thread pooling
``` python
from multiprocessing import cpu_count, set_start_method
from multiprocessing.pool import ThreadPool as Pool

set_start_method("spawn")

n_threads = int(cpu_count()/4)
with Pool(n_threads) as pool:

    pool_result = pool.map_async( # just use map_async for mapping
        self.convert_new, # method to call in paralell
        file_list # list of parameters
    )
    pool_result.wait()
```
 The called method can look like:
 ``` python
def convert_new(
        self,
        file_info: str
    ) -> None:
    # do something
    ...
    # then alter a class predefined array/dictionary
    self.key_data[key].extend(json_data)
```

<br>   

# Interact with a REST API
``` python
import json
import requests



def _send_request(self,
                      request_type: str,
                      url: str,
                      **kwargs) -> requests.Response:
        """
        Send a request to the REST API.
        :param request_type: Request type (GET, POST, PUT etc.).
        :param url: The URL against which the request needs to be made.
        :return: requests.Response
        """
        if not self.header:
            self.header = {'Authorization': f'Bearer {self._get_token()}'}

        request_funcs = {
            'GET': requests.get,
            'POST': requests.post
        }

        func = request_funcs.get(request_type.upper())

        if not func:
            raise Exception(
                  f'Request type of {request_type.upper()} not supported.'
            )

        r = func(url=url, headers=self.header, **kwargs)
        r.raise_for_status()
        return r
```

<br>   

# Join together (concatenate) csv files and write csv with pandas

__Comment__: use the shebang (start) of the script to define that the script should be run with python if directly called without the preceding language (no python bla.py)
``` python
#!/usr/bin/env python3  

import os
import glob # unix like path extention: e.g. **/*123.csv
import pandas as pd

#spefify your new working directory
os.chdir("/home/acu/some_files")

# get dates from the 05 to the 28
for i in range(5,28):
    # define date base in file name out of i and do some right padding
    x = '*.202005' + str(i).rjust(2, '0') + '*'
    all_filenames = [i for i in glob.glob(x)] 

    # concatenate all files found with the glob expression
    # concat the list of dataframes
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    file_name = 'combined_date_csv.csv'
    # export to csv
    combined_csv.to_csv(file_name, index=False, encoding='utf-8-sig')

    # remove processed files
    for f in all_filenames:
        os.remove(f)
```
