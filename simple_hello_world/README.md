### Getting started

Set up your env as below then run this hello world example. Feel free to clone this repo, branch, etc.

```
# Example setting up virtualenv and writing requirements
cd class102
virtualenv ~/.virtualenvs/class102
source ~/.virtualenvs/class102/bin/activate

export PIP_PROXY=<ip:port>
pip install --proxy ${PIP_PROXY} pip --upgrade
pip install --proxy ${PIP_PROXY} django
pip freeze | egrep -i django | tee requirements.txt

pip install --proxy ${PIP_PROXY} gunicorn
pip freeze |egrep gunicorn | tee -a requirements.txt

gunicorn hello -b 0.0.0.0:8888

# Now view this at <your fqdn:8888>

```

#### Homework
* Add a new url pattern and a function to display new content

#### Comments
* This first example is [stolen shameless from ... ](https://github.com/lightweightdjango/examples/blob/chapter-1/hello.py)
which is an awsome book, though now somewhat outdated
* You can see that the django library is handling the requests and responses
* If you want to see a pure python, handling requests, headers, etc. see the first 
example here: [Pure Python](http://dfpp.readthedocs.io/en/latest/chapter_01.html)
