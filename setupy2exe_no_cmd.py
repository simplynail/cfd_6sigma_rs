# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:14:10 2016

@author: pawel.cwiek
"""


from distutils.core import setup
import py2exe
import sip
import leather

setup(windows=['6SigmaRS.py'], options={"py2exe":{"includes":["sip","leather"],'excludes':['requests','matplotlib','doctest','pdb','unittest','difflib','inspect','nbformat','jinja2','numpy','PyQt5','nose','colorama','argparse','pydoc','asyncio','OpenGL','tornado','zmq']}})