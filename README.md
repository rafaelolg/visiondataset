
# Visiondataset Project #

## About ##

Vision dataset computer vision datasets management system.

## Prerequisites ##

- Python >= 2.5
- pip
- virtualenv (virtualenvwrapper is recommended for use during development)

## Installation ##

### Inside local Vitual Machine ###
You can run as into its integrated virtual machine. To do that, first you need to install [vagrant][Vagrant] and also [virtualenv][virtualenv]

    pip install fabric
    vagrant up
    fab dev setup

This will take awhile (like, awhile). You may be prompted for input during the fab dev bootstrap step, so you will need to bear it out.

When the initial setup is finished, you will have a running server instance at localhost:8000.

### Dev Requirements ###

	cp ./visiondataset/settings/local-dist.py ./visiondataset/settings/local.py
	$EDITOR ./visiondataset/settings/local.py #edit local.py
	pip install -r requirements/all.txt
	./manage.py syncdb
	./manage.py migrate
	./manage.py runserver

### Ubuntu Production ###
Install de developer requirements and then  edit add the host variables into environments.py file. 

    def production():
       with common():
          env.user = 'foo'
          env.hosts = ['bar']
          env.domain = 'visiondataset.domain'


License
-------
This software is licensed under the [GPLv3][GPL]. For more
information, read the file ``LICENSE``.

[GPL]: http://www.gnu.org/copyleft/gpl.html
[vagrant]: http://vagrantup.com
[virtualenv]: http://www.virtualenv.org
