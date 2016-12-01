#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# =========================================
# Projet:	PyJoke
# Rôle:		Gère les échanges réseau
# Crée le:	01/12/2016
# =========================================
from config import *
import json
import socket

class Exchange:
	def __init__( self ):
		self.data = dict()

	# Ajoute une clef à l'échange (écrase la valeur si elle existe déjà)
	#
	# -?-
	# [str] key:	Nom de la clef
	# [?] value:	Valeur associé
	# -$-
	# TypeError		! -?-
	def add( self, key, value ):
		if( not isinstance( key, str ) ):
			raise TypeError( '! -?-' )

		self.data[ key ] = value

	# Retourne la valeur associé à une clef
	#
	# -?-
	# [str] key:	Nom de la clef
	# -!-
	# [?]
	# -$-
	# [TypeError]	! -?-
	# [KeyError]	Si <key> n'existe pas
	def get( self, key ):
		if( not isinstance( key, str ) ):
			raise TypeError( '! -?-' )
		elif( not key in self.data ):
			raise KeyError( '<key> n\'existe pas !' )

		return self.data[ key ]

	# Supprime une clef et retourne sa valeur associé
	#
	# -?-
	# [str] key:	Nom de la clef
	# -!-
	# [?]
	# -$-
	# [TypeError]	! -?-
	# [KeyError]	Si <key> n'existe pas
	def remove( self, key ):
		if( not isinstance( key, str ) ):
			raise TypeError( '! -?-' )
		elif( not key in self.data ):
			raise KeyError( '<key> n\'existe pas !' )

		return self.data.pop( key )

	# Retourne la liste des clefs
	#
	# -!-
	# [dict]
	def getAll( self ):
		return dict( self.data )

	# //////////////
	# /// RESEAU ///
	# //////////////

	# Envoie les données via le socket spécifié
	#
	# -?-
	# [socket] sock:	Socket à utiliser
	# -!-
	# [bool]
	# -$-
	# TypeError 		! -?-
	def send( self, sock ):
		if( not isinstance( sock, socket.socket ) ):
			raise TypeError( '! -?-' )

		try:
			data = json.dumps( self.data )
			sock.send( data )
			return True
		except ( ValueError, socket.error ):
			return False

	# Reçoit des données via le socket spécifié
	#
	# -?-
	# [socket] sock:	Socket à utiliser
	# -!-
	# [bool]
	# -$-
	# TypeError 		! -?-
	def recv( self, sock ):
		if( not isinstance( sock, socket.socket ) ):
			raise TypeError( '! -?-' )

		try:
			data = sock.recv( CONFIG['NTWBUFSIZE'] )
			data = json.loads( data )
			self.data = data
		except ( ValueError, socket.error ):
			return False

		return True

	# Purge les clefs et valeurs
	def purge( self ):
		self.data = dict()
