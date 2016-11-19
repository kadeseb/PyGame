#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ========================================
# Projet:	PyJoke
# Rôle:		Configuration du programme
# Crée le:	09/10/2016
# ========================================
import json

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

		print '| Lecture du fichier de configuration (%s)...' % ( configFile )
		try:
			configFile = open( 'config.json', 'r' )
			configStr = configFile.read()
		except IOError:
			print '$ Erreur: Impossible d\'accéder au fichier de configuration'
			raise SystemError()
		print '$ Ok'

		print '| Extraction des informations de configuration...'
		try:
			self.config = json.loads( configStr )
		except TypeError:
			print '$ Erreur: Le fichier est invalide !'
			raise SystemError( 'Impossible de charger le fichier de configuration !' )
		print '$ Ok'

	def get( self ):
		return self.config

configuration = Configuration( 'config.json' )
CONFIG = configuration.get()

CONFIG = {
	'WINDOWS_NUMBER': 1,
	'WINDOWS_POSUPDATEINTERVAL': 1000,
	'WINDOWS_WIDTH': 500,
	'WINDOWS_HEIGHT': 500,
	'IMAGES_DIR': 'img/',
	'SOUNDS_DIR': 'sound/',
	'PORT': 2048,
	'TIMEOUT': 5,
	'CMDIDSIZE': 8,
	'NTWBUFSIZE': 4096,
	'SALTSIZE': 10,
	'LOGINTRYCOUNT': 3,
	'PASSWORD': 'password'
}
