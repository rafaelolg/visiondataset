#!/bin/sh

#
# bin/bootstrap.sh
#
# Developed by Rafael de O. Lopes Gonçalves <>
# Copyright (c) 2012 
# Licensed under terms of GNU General Public License.
# All rights reserved.
#
#
# Changelog:
# Created: 28 de maio de 2012
# Last Change: 28 de maio de 2012
pip install -r requirements/all.txt
vagrant up
fab vagrant setup
./manage.py syncdb

