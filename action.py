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
import display as Dispay
from Tkinter import *
import sound as Sound
from functions import *

class Manager:
	##
	# Constructeur
	##
	def __init__( self ):
		# Initialisation de l'objet
		self.displayManager = Dispay.Manager()
		self.soundManager = Sound.Manager()
		self.responseBuffer = ''
		self.exiting = False

		# Association des commandes aux callbacks
		self.command = {
			'soundlist': self.CMD_soundlist,
			'sl': self.CMD_soundlist,
			'play': self.CMD_playsound,
			'p': self.CMD_playsound,
			'eject': self.CMD_eject,
			'quit': self.CMD_exit,
			'q': self.CMD_exit,
			'display': self.CMD_display,
			'd': self.CMD_display,
			'h': self.CMD_help
		}

	##
	# Execute une commande
	# -?-
	# command 	[str] Commande à exécuter
	# -!-
	# [bool] 	La commande s'est executé correctement
	##
	def execute( self, command ):
		self.responseBuffer = ''
		command = command.lower()
		args = command.split( ' ' )

		try:
			return self.command[ args[ 0 ] ]( args )
		except KeyError:
			self.error( 3 )
			return False

	##
	# Créer un message d'erreur
	# -?-
	# [int] code 	Code erreur
	##
	def error( self, code ):
		if code == 1:
			self.addResponse( 'ERREUR: Argument incorrect !' )
		elif code == 2:
			self.addResponse( 'ERREUR: Element spécifié introuvable !' )
		elif code == 3:
			self.addResponse( 'ERREUR: Commande introuvable !' )

	##
	# Effectue des actions
	##
	def action( self ):
		self.displayManager.ExecuteQueue()
		self.soundManager.performPlaylist()

	def askExit( self ):
		return self.exiting

	##
	# Retourne le contenu du tampon de réponse
	# -!-
	# [string]
	##
	def getResponse( self ):
		if( len( self.responseBuffer ) == 0 ):
			return 'OK'

		return self.responseBuffer[:-1]

	def addResponse( self, response ):
		self.responseBuffer += response + '\n'

	# ------------
	# > Commande <
	# ------------
	# > Liste les sons disponibles
	def CMD_soundlist( self, command ):
		soundList = self.soundManager.getSoundList()

		self.addResponse( 'Liste des son(s) disponible(s):' )
		self.addResponse( '[ID]\t[NOM]' )

		for i in xrange( 0, len( soundList ) ):
			self.addResponse( '%d\t%s' % (i, soundList[i]) )

		return True

	# > Joue un son
	def CMD_playsound( self, command ):
		# Extraction de l'ID du son
		if( len( command ) < 2 ):
			self.error( 1 )
			return False
		elif( not strIsInt( command[1] ) ):
			self.error( 1 )
			return False
		else:
			soundID = int( command[1] )

		# Extraction du nombre de lecture
		if( len( command ) < 3 ):
			playCount = 1
		elif( not strIsInt( command[2] ) or int( command[2] ) <= 0 ):
			self.error( 1 )
			return False
		else:
			playCount = int( command[2] )

		# Extraction du delais
		if( len( command ) < 4 ):
			nextDelay = 0
		elif( not strIsInt( command[3] ) or int( command[2] ) < 0 ):
			self.error( 1 )
			return False
		else:
			nextDelay = int( command[3] )

		# Ajout des sons
		for i in xrange( 0, playCount ):
			error = not self.soundManager.playlistAdd( soundID, nextDelay )

			if( error ):
				self.error( 1 )
				return False

		return True

	# > Ejecte le lecteur CD
	def CMD_eject( self, command ):
		subprocess.Popen('eject')
		return True

	# > Quitte le programme
	def CMD_exit( self, command ):
		self.exiting = True
		self.addResponse( 'Bye ;)' )

		return True

	# > Permet de gérer l'affichage
	def CMD_display( self, command ):
		self.addResponse( 'Réponse aquise !' )
		self.addResponse( str( self.displayManager.PushCommand( command[1:] ) ) )

		return True

	# > Affiche l'aide
	def CMD_help( self, command ):
		self.addResponse( 'Liste des commandes: ' )
		for command in self.command:
			self.addResponse( command )
