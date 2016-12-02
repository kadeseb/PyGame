#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ========================================
# Projet:	PyBlague
# Rôle:		Regroupe les fonctions
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ========================================
import ast
from random import randrange

# Vérifie qu'une chaine représente un int
#
# -?-
# [str] string:		Chaine à tester
# -!-
# [bool]
def strIsInt( string ):
	try:
		value = int( string )
		return True
	except ValueError:
		return False

def strToDict( string ):
	return ast.literal_eval( string )

# Génére une chaine de caractère aléatoire
#
# -?-
# [int] size 	Taille de la chaine à générer
 # -!-
 # [str] / [None]
def randomAlphaNumStr( size ):
	if( not isinstance( size, int ) or size <= 0 ):
		return None

	charList = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	randomStr = ''

	for count in xrange( 0, size ):
		randomStr += charList[ randrange( 0, len( charList ) ) ]

	return randomStr

# Vérifie si un port est valide
#
# -?-
# [int/string] port 	Port à tester
# -!-
# [bool]				Le port est valide
def portIsValid( port ):
	if( not isinstance( port, int ) and not isinstance( port, str ) ):
		return False

	if( isinstance( port, str ) ):
		try:
			port = int( port )
		except ValueError:
			return False

	return ( port > 0 ) and ( port < 65535 )
