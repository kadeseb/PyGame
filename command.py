#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ========================================
# Projet:	PyJoke
# Rôle:		Gestion des commandes
# Crée le:	09/10/2016
# ========================================
from threading import Thread, RLock
import re
import random
import bank as Bank
import display as Display
import sound as Sound
from functions import *
from commandclass import *
from config import *

lock = RLock()

class Manager( Thread ):
	COMMAND = {
		'exit': 'Command_Exit',
		'quit': 'Command_Quit',
		'help': 'Command_Help',
		'sound': 'Command_Sound',
		'eject': 'Command_Eject',
		'window': 'Command_Window'
	}
	COMMAND_STATE = {
		'AWAITING': 0,
		'PERFORMED': 1
	}

	# Constructeur
	def __init__( self ):
		#Thread.__init__( self )

		self._CTX_ = {
			'DISPLAY': Display.Manager(),
			'SOUND': Sound.Manager(),
			'EXITING': False,
			'COMMAND': self.COMMAND,
			'DISCONNECT': False
		}

		self.commandQueue = {}
		self.commandResult = {}

	# Lancement du thread
	def run( self ):
		while not self.exiting():
			self.action()

	# Créer une association entre une commande et une classse
	#
	# -?-
	# [str] command: 	Commande
	# [str] class: 		Classe de la commande
	# -!-
	# [bool]
	'''
	def associate( self, command, classCMD ):
		if( ( not re.match( '^\w+$', command ) ) or ( not re.match( '^\w+$', classCMD ) ) ):
			return False

		try:
			eval( classCMD )
		except NameError:
			return False

		self.COMMAND[ command ] = classCMD
		return True
	'''

	# Envoie une commande dans la liste d'exécution
	#
	# -?-
	# [str] command:		Commande à envoyer
	# -!-
	# [str]					Identifiant unique de la commande
	def put( self, command ):
		with lock:
			while True:
				commandID = randomAlphaNumStr( CONFIG['SALTSIZE'] )

				if not commandID in self.commandQueue:
					break

			self.commandQueue[ commandID ] =  {
					'COMMAND': command,
					'STATE': Manager.COMMAND_STATE['AWAITING']
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
		if( not isinstance( commandID, str ) ):
			raise TypeError

		with lock:
			try:
				container = self.commandQueue[ commandID ]
			except KeyError:
				return None

			if( container['STATE'] == Manager.COMMAND_STATE['PERFORMED'] ):
				self.commandQueue.pop( commandID )
				return self.commandResult.pop( commandID )
			else:
				return None

	# Effectue les actions en attente
	def action( self ):
		with lock:
			# Commande en attente
			for identifiant, container in self.commandQueue.iteritems():
				command = container['COMMAND'].split()

				if( container['STATE'] == Manager.COMMAND_STATE['PERFORMED'] ):
					continue

				if( len( command ) and command[0] in self.COMMAND ):
					commandObject = self._getObjectFromName(command[0] )
					commandObject.__execute__( command[1:], self._CTX_ )

					self.commandResult[ identifiant ] = commandObject.__result__()
				else:
					self.commandResult[ identifiant ] = {
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

	# Demande l'arrêt du programme
	def quit( self ):
		self._CTX_['EXITING'] = True

	# Retoune une instance de la classe spécifié
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
