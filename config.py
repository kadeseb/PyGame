#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ========================================
# Projet:	PyJoke
# Rôle:		Configuration du programme
# Crée le:	09/10/2016
# ========================================
import json

DEBUG = False

class Configuration:
	# Charge le fichier de configuration
	#
	# -?-
	# [str] configFile:		Chemin du fichier de configuration
	# -$-
	# [TypeError]			Si <configFile> n'est pas de type str
	def __init__( self, configFile ):
		if( not isinstance( configFile, str ) ):
			raise TypeError( '<configFile> n\'est pas de type [str] !' )

		if DEBUG: print '| Lecture du fichier de configuration (%s)...' % ( configFile )
		try:
			configFile = open( 'config.json', 'r' )
			configStr = configFile.read()
		except IOError:
			print '$ Erreur: Impossible d\'accéder au fichier de configuration'
			raise SystemError()
		if DEBUG: print '$ Ok'

		if DEBUG: print '| Extraction des informations de configuration...'
		try:
			self.config = json.loads( configStr )
		except TypeError:
			print '$ Erreur: Le fichier est invalide !'
			raise SystemError( 'Impossible de charger le fichier de configuration !' )
		if DEBUG: print '$ Ok'

	def get( self ):
		return self.config

configuration = Configuration( 'config.json' )
CONFIG = configuration.get()
