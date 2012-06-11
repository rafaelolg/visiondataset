#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

def base_name(filename):
    """
    return the string filename without extensions nor directory path
    >>> base_name('asdf.tar.gz')
    'asdf'
    >>> base_name('/root/ver_strange.dir/asdf.tar.gz')
    'asdf'
    >>>  base_name(r'c:\Windows With Spaces\asdf.tar.gz')
    'asdf'
    """
    s = re.split(r'[\\|/]', filename)[-1]
    s = re.split(r'\.', s)[0]
    return s


def extension_name(filename):
    """
    return the extension of the file
    >>> extension_name('asdf.tar.gz')
    'jpg'
    >>> extension_name('/root/ver_strange.dir/asdf.tar.gz')
    'jpg'
    >>>  extension_name(r'c:\Windows With Spaces\asdf.tar.gz')
    'tar.gz'
    """
    s = re.split(r'[\\|/]', filename)[-1]
    s =  '.'.join(s[1:])
    return s

# util.py
