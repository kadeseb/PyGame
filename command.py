#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Gestion des commandes
# Crée le:	09/10/2016
# ----------------------------------------
import re
import random
import bank as Bank
import display as Display
import sound as Sound
from functions import *
from commandclass import *
from config import *

class Manager:
	COMMAND = {
		'quit':'Command_Quit',
		'help':'Command_Help'
	}
	COMMAND_STATE = {
		'AWAITING': 0,
		'PERFORMED': 1
	}

	# Constructeur
	def __init__( self ):
		self._CTX_ = {
			'DISPLAY': Display.Manager(),
			'SOUND': Sound.Manager(),
			'EXITING': False,
			'COMMAND': self.COMMAND
		}

		self.commandQueue = {}

	# Associe une nouvelle commande
	#
	# -?-
	# [str] command: 	Commande
	# [str] class: 		Classe de la commande
	# -!-
	# [bool]
	def associate( self, command, classCMD ):
		if( ( not re.match( '^\w+$', command ) ) or ( not re.match( '^\w+$', classCMD ) ) ):
			return False

		try:
			eval( classCMD )
		except NameError:
			return False

		self.COMMAND[ command ] = classCMD
		return True

	# Envoie une commande dans la liste d'exécution
	#
	# -?-
	# [str] command:		Commande à envoyer
	# -!-
	# [str]					Identifiant unique de la commande
	def put( self, command ):
		while True:
			commandID = self.generateID()

			if not commandID in self.commandQueue:
				break

		self.commandQueue[ commandID ] =  {
				'COMMAND': command,
				'STATE': Manager.COMMAND_STATE['AWAITING'],
				'RESULT': None
			}

		return commandID

	# Renvoie le résultat d'une commande
	#
	# -?-
	# [string] commandID:	ID de la commande ciblé
	#
	# -!-
	# [dict] / None 		Résulat de la commande
	def get( self, commandID ):
		if( commandID in self.commandQueue ):
			container = self.commandQueue[ commandID ]

			if( container['STATE'] == Manager.COMMAND_STATE['PERFORMED'] ):
				return self.commandQueue.pop( commandID )['RESULT']
			else:
				return None
		else:
			return None

	# Génère un identifiant de commande
	#
	# -!-
	# [str]
	def generateID( self ):
		charList = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
		id = ''

		for i in xrange( 0, CONFIG['CMDIDSIZE'] ):
			id += charList[ random.randrange( 0, len( charList ) ) ]

		return id

	# Effectue les actions en attente
	def action( self ):
		# Commande en attente
		for identifiant, container in self.commandQueue.iteritems():
			command = container['COMMAND'].split()

			if( len( command ) and command[0] in self.COMMAND ):
				commandObject = self._getObjectFromName(command[0] )
				commandObject.__execute__( command[1:], self._CTX_ )
				container['RESULT'] = commandObject.__result__()
			else:
				container['RESULT'] = {
					'CODE': Command._CODE_['BADCMD'],
					'STATUS': Command._CODE_STATUS_[ Command._CODE_['BADCMD'] ],
					'OUTPUT': ''
				}

			container['STATE'] = Manager.COMMAND_STATE['PERFORMED']

		# Mise à jour des autres gestionnaires
		self._CTX_['SOUND'].performPlaylist()
		self._CTX_['DISPLAY'].update()

	# Retourne l'état du programme
	def exiting( self ):
		return self._CTX_['EXITING' ]

	# Retounr une instance de la classe spécifié
	#
	# -?-
	# [str] name:	Nom de la commande
	# -!-
	# [~Command] / [None]
	def _getObjectFromName( self, name ):
		if( not re.match( '^\w+$', name ) ):
			return None

		try:
			return eval( self.COMMAND[ name ] + '( "%s" )' % name )
		except NameError:
			return None
