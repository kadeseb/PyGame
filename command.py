#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Interprète les commandes
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ----------------------------------------
import subprocess
import bank as Bank
import display as Display
from Tkinter import *
import sound as Sound
import argparse
from docopt import docopt, DocoptExit
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

	##
	# Constructeur
	##
	def __init__( self ):
		self._ENV_ = {
			'DISPLAY': Display.Manager(),
			'SOUND': Sound.Manager(),
			'EXITING': False
		}
		self.commandQueue = {}

	##
	# Envoie une commande dans la liste d'exécution
	# -?-
	# [string] command:		Commande à envoyer
	# -!-
	# [str]					Identifiant unique de la commande
	##
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

	##
	# Renvoie le résultat d'une commande
	# -?-
	# [string] commandID:	ID de la commande ciblé
	# -!-
	# [dict] / None 		Résulat de la commande
	##
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

	##
	# Execute les commandes en attente
	##
	def performCommand( self ):
		for identiant, container in self.commandQueue.iteritems():
			command = container['COMMAND'].lower().split()

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

	##
	# Effectue des actions
	##
	def action( self ):
		self.performCommand()

		# Autres gestionnaires
		self._ENV_['SOUND'].performPlaylist()

		#self.displayManager.update()

# ///////// #
# Commandes #
# ///////// #
class Command:
	_FORMAT_ = 'Usage: $CMD'
	_CODE_ = {
		'OK': 0,
		'BADCMD': 1,
		'BADARG': 2,
		'NOTFOUND': 3,
		'INVALIDCODE': 4
	}
	_CODE_STATUS_ =  {
		0: "OK",
		1: "Commande invalide",
		2: "Argument incorrect",
		3: "Element non trouvé",
		4: "Code invalide"
	}

	def __init__( self, name ):
		self._FORMAT_ = self._FORMAT_.replace( '$CMD', name )
		self.code = Command._CODE_[ 'OK' ]
		self.output = ''

	def __execute__( self, args, commandManager ):
		try:
			args = docopt( self._FORMAT_, argv=args, options_first=False )
		except DocoptExit:
			self.code = Command._CODE_[ 'BADARG' ]
			self.output = self._FORMAT_
			return

		self.action( args, commandManager )

	def __result__( self ):
		if( self.code in Command._CODE_STATUS_ ):
			status = Command._CODE_STATUS_[ self.code ]
			code = self.code
		else:
			code = Command._CODE_[ 'INVALIDCODE' ]
			status = Command._CODE_STATUS_[ code ]

		return {
			'CODE': code,
			'STATUS': status,
			'OUTPUT': self.output
		}

	def action( self, commandManager ):
		print 'OK'


# -> Ferme le programme
class Command_Quit( Command ):
	def action( self, arguments, commandManager ):
		commandManager['EXITING'] = True
		self.output += 'Arrêt du serveur'

# -> Affiche l'aide
class Command_Help( Command ):
	def action( self, arguments, commandManager ):
		print arguments
		self.output = 'Affiche l\'aide'

# -> Ouvre le lecteur CD
class Command_Eject( Command ):
	def action( self, arguments, commandManager ):
		subprocess.Popen( 'eject' )
		self.output += 'Lecteur CD ouvert'

# -> Gère la lecture de son
class Command_Sound( Command ):
	_FORMAT_ = 	'Usage:\n'
	_FORMAT_ += '	$CMD list\n'
	_FORMAT_ += '	$CMD play <id> [<count>] [<delais>]\n'
	_FORMAT_ += '	$CMD purge'

	def action( self, arguments, commandManager ):
		# Liste les sons disponibles
		if( arguments['list'] ):
			soundList = commandManager['SOUND'].getSoundList()

			self.output += 'Liste des sons:\n'
			self.output += '[ID]\t[Fichier]'

			for soundID in xrange( 0, len( soundList ) ):
				self.output += '\n%d\t\t%s' % ( soundID, soundList[ soundID ] )

			self.code = Command._CODE_['OK']

		# Joue un son
		elif( arguments['play'] ):
			# ID du son
			if( not commandManager['SOUND'].validSound( arguments['<id>'] ) ):
				self.code = Command._CODE_['NOTFOUND']
				self.output = 'Le son spécifié n\'existe pas !'
				return
			else:
				soundID = int( arguments['<id>'] )

			# Nombre de lecture
			if( arguments['<count>'] ):
				if( strIsInt( arguments['<count>'] ) ):
					count = int( arguments['<count>'] )
				else:
					self.code = Command._CODE_['BADARG']
					return
			else:
				count = 1

			# Delais
			if( arguments['<delais>'] ):
				if( strIsInt( arguments['<delais>'] ) ):
					delais = int( arguments['<delais>'] )
				else:
					self.code = Command._CODE_['BADARG']
					return
			else:
				delais = 0

			for i in xrange( 0, count ):
				commandManager['SOUND'].playlistAdd( soundID, delais )

			self.code = Command._CODE_['OK']

		# Purge la playlist
		elif( arguments['purge'] ):
			commandManager['SOUND'].playlistPurge()
			self.code = Command._CODE_['OK']
			self.output = 'Playlist correctement purgée !'

# -> Gère l'affichage de fenêtre
class Command_Window( Command ):
	_FORMAT_ = 	'Usage: \n'
	_FORMAT_ += '	$CMD list (image | window)\n'
	_FORMAT_ += '	$CMD create [options] [<count>]\n'
	_FORMAT_ += '	$CMD set [options] <windowID>... \n'
	_FORMAT_ += '	$CMD close [all | (<windowsID>...)]\n'
	_FORMAT_ += '\n'
	_FORMAT_ += 'Options:\n'
	_FORMAT_ += '-r=(1 | 0) --randomizePosition=(1 | 0)	Position de la fenêtre aléatoire\n'
	_FORMAT_ += '-i=IMAGE --image=IMAGE 		Image de la fênetre\n'
	_FORMAT_ += '-t=TITLE --title=TITLE 		Titre de la fênetre'

	def action( self, arguments, commandManager ):
		print arguments

		# Liste des images/fenêtre
		if( arguments['list'] ):
			if( arguments['image'] ):
				imageList = commandManager['DISPLAY'].getImageBank().getList()

				self.output += 'Liste des images:\n'
				self.output += '[ID]\t[Taille]\t[Nom]'

				for imageID in xrange( 0, len( imageList ) ):
					size = '%dx%d' % ( imageList[imageID]['width'], imageList[imageID]['height'] )
					name = imageList[imageID]['name']

					self.output += '\n%d\t\t%s\t\t%s' % ( imageID, size, name  )

				self.code = Command._CODE_['OK']
				return

		# Création d'une fenêtre
		elif( arguments['create'] ):
			if( arguments['--image'] ):
				if( arguments['--image'] == '?' ):
					image = None
				elif( strIsInt( arguments['--image'] ) ):
					image = int( arguments['--image'] )
				else:
					self.code = Command._CODE_['BADARG']
					return
			else:
				image = None

			if( arguments['--title'] ):
				title = arguments['--title']
			else:
				title = None

			if( arguments['--randomizePosition'] ):
				randomizePosition = bool( int (arguments['--randomizePosition'] ) )
			else:
				randomizePosition = True

			configuration = {
				'IMAGE': image,
				'RANDOMIZEPOS': randomizePosition,
				'TITLE': title
			}

			print configuration

			if( arguments['<count>'] ):
				if( strIsInt( arguments['<count>'] ) ):
					windowCount = int( arguments['<count>'] )
				else:
					self.code = Command._CODE_['BADARG']
					return
			else:
				windowCount = 1

			for i in xrange( 0, windowCount ):
				commandManager['DISPLAY'].createWindow( configuration )
