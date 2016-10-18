#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Gestion des commandes
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ----------------------------------------
from commandclass import *
import subprocess
import bank as Bank
import display as Display
from Tkinter import *
import sound as Sound
import random
from functions import *

class Manager:
	COMMAND = {
		'quit': 'Command_Quit',
		'eject': 'Command_Eject',
		'help': 'Command_Help',
		'sound': 'Command_Sound',
		'window': 'Command_Window'
	}

	COMMAND_STATE = {
		'AWAITING': 0,
		'PERFORMED': 1
	}

	COMMAND_CODE = {
		'OK': 0,
		'BADCMD': 1,
		'BADARG': 2,
		'NOTFOUND': 3
	}

	# Constructeur
	def __init__( self ):
		self._ENV_ = {
			'DISPLAY': Display.Manager(),
			'SOUND': Sound.Manager(),
			'EXITING': False
		}
		self.commandQueue = {}

	# Envoie une commande dans la liste d'exécution
	# -?-
	# [string] command:		Commande à envoyer
	# -!-
	# [str]					Identifiant unique de la commande
	def send( self, command ):
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
	# -?-
	# [string] commandID:	ID de la commande ciblé
	# -!-
	# [dict] / None 		Résulat de la commande
	def get( self, commandID ):
		if( commandID in self.commandQueue ):
			container = self.commandQueue[ commandID ]

			if( container['STATE'] == Manager.COMMAND_STATE['PERFORMED'] ):
				result = self.commandQueue.pop( commandID )['RESULT']
				return result
			else:
				return None

	def generateID( self ):
		charList = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
		size = 8
		id = ''

		for i in xrange( 0, size ):
			id += charList[ random.randrange( 0, len( charList ) ) ]

		return id

	# Execute les commandes en attente
	def performCommand( self ):
		for identifiant, container in self.commandQueue.iteritems():
			command = container['COMMAND'].split()

			if( len( command ) and command[0] in self.COMMAND ):
				call = self.COMMAND[ command[0] ] + '( "%s" )' % command[0]
				commandObject = eval( call )

				commandObject.__execute__( command[1:], self._ENV_ )
				container['RESULT'] = commandObject.__result__()
			else:
				container['RESULT'] = {
					'CODE': Command._CODE_['BADCMD'],
					'STATUS': Command._CODE_STATUS_[ Command._CODE_['BADCMD'] ],
					'OUTPUT': ''
				}

			container['STATE'] = Manager.COMMAND_STATE['PERFORMED']

	# Effectue des actions
	def action( self ):
		self.performCommand()

		# Autres gestionnaires
		self._ENV_['SOUND'].performPlaylist()

		#self.displayManager.update()
