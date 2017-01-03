# `jcs-python-sdk-sbs-tester`
=============================

This is a tester project for the project `jcs_python_sdk_sbs`.


Before running this project:
============================


Install the parent project:
---------------------------

- 
Clone or download the parent project from *git@github.com:utsav-deep-rjil/jcs-python-sdk-sbs.git*

- 
Setup a virtual environment using command *virtualenv your_env_name* and activate it using *source your_env_name/bin/activate*

- Now in virtualenv, go to the root directory of the parent project and run the command
*python setup.py install* to install the parent project *jcs-python-sdk-sbs*


CA-CERTIFICATE INSTALLATION:
----------------------------

- 
**Get the ca-certificate for JIO cloud services from JIO Cloud Team and install it**

- For Linux : Place the ca-certificate inside the folder 
*/usr/local/share/ca-certificates/* and then run *update-ca-certificates --fresh* in terminal

- For Mac : 
- For Windows :


Setting up the Project:
-----------------------

The following properties must be set for proper working of this SDK:

- BASE_URL
- ACCESS_KEY
- SECRET_KEY

You can set these properties in any of the following locations:

- OS Environment Variables
- In 
*config.properties* file under *fixtures* folder of this project. The content of this file must be like this:

```
[dev]
ACCESS_KEY=*JCSAccessKey of staging*
SECRET_KEY=*JCSScretKey of staging*
BASE_URL=*endpoint or base url of staging*

[prod]
ACCESS_KEY=*JCSAccessKey of production*
SECRET_KEY=*JCSScretKey of production*
BASE_URL=*endpoint or base url of production*

[branch]
# change this to point the script at a specific environment
env=dev
```


Running the project:
--------------------

Run the *__init__.py* file of *sbs_tester.jcs_service* package as *python unit-test*.


