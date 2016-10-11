#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Regroupe les fonctions
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ----------------------------------------

def strIsInt( string ):
	try:
		value = int( string )
		return True
	except ValueError:
		return False