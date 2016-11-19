#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyJoke
# Rôle:		Gère le protocole réseau
# Crée le:	21/10/2016
# ----------------------------------------
import urllib
import json
import socket
import hashlib
import threading
from config import *
from functions import *

def Request:
    def __init__( self ):
        self.ready = False

        
