from __future__ import with_statement
from contextlib import contextmanager as _contextmanager
from fabric.contrib.files import exists, append, upload_template, sed
from fabric.contrib.project import rsync_project
from fabric.api import *
from fabric.colors import *
from environments import *
#from pprint import pprint
#import urllib2

@_contextmanager
def vagrant_env():
	with cd("$VAGRANT_ROOT"):
		with prefix('workon %s' % env.project_name):
			yield


MEDIA_ROOT = 'upload/'

def fetch_file(item):
	url, fname = item
	with vagrant_env():
		run("curl -o %s%s %s" % (MEDIA_ROOT, fname, url))


def fetch_files():
	map(lambda f: fetch_file(f), FILES)

