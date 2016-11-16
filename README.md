# lingglemt-django (standalone)
Linggle Machine Translation Web System (standalone distribution)

Note: This is standalone version which does not require **lingglemt-core** and **redis**. It should be easier to build.

## Prerequisite
- Essential
  - python
  - Django
  - requests

## Get started
### Create virtual environment (py3 recommended)
There are a lot problems of dependencies versions, and indirectly permissions in Python.
It is strongly recommended to use tools like [virtualenv](https://virtualenv.pypa.io).
Here's an example using **virtualenv**.
```console
$ virtualenv lmtenv --python=python3
$ source lmtenv/bin/activate
```

### Run the system
Clone the repository
```console
$ git clone https://github.com/NTHU-NLPLAB/lingglemt-django
$ cd lingglemt-django
```

Install necessary python packages from `requirement.txt`
```console
$ pip install -r requirements.txt
```

Then, you are good to go. Just enter the following command:
```console
$ python manage.py runserver 0.0.0.0:5566
```
(note: you might have to set`DEBUG = False` under `linggletranslate/settings.py`.)
