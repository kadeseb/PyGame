#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Gère l'affichage de fenêtre
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ----------------------------------------
import random
import PIL.Image
import PIL.ImageTk
from Tkinter import *
from functions import *
from bank import *

class Manager:
	STATUSCODE = {
		'OK': 0,
		'BADCMD': 1,
		'BADARG': 2
	}

	def __init__( self ):
		# Initialisation de TkInter
		self.tk = Tk( )
		self.tk.wm_title(' ')
		self.tk.withdraw()

		# Initialisation de l'object
		self.imageBank = ImageBank()
		self.windowList = []
		self.commandQueue = []

		self.mode = {
			'cw': self.MODE_CreateWindow
		}

	# Execute une commande
	# -?-
	# [list] command:	Commande à exécuter
	def Execute( self, command ):
		try:
			self.mode[ command[0] ]( command[1:] )
		except IndexError:
			return Manager.STATUSCODE['BADCMD']

		return Manager.STATUSCODE['OK']

	# Ajoute une commande dans la liste
	# -?-
	# [list] command:	Commande à ajouter
	def PushCommand( self, command ):
		# Vérifie la commande
		try:
			returnCode = self.mode[ command[0] ]( command[1:], True )

			# Ajoute la commande dans la liste
			self.commandQueue.append( command )

			print 'push'
			print self.commandQueue

			return returnCode
		except IndexError:
			return Manager.STATUSCODE['BADCMD']

	# Rafraichie les fenêtres
	def Update( self ):
		for windowID in xrange( 0, len( self.windowList ) ):
			self.windowsList[ windowID ].update()


	# Execute les commandes en attente
	def ExecuteQueue( self ):
		#print self.commandQueue

		for commandID in xrange( 0, len( self.commandQueue ), 1 ):
			print 'triaiter'
			command = self.commandQueue.pop()
			self.mode[ command[0] ]( command[1:] )
			command.pop()

		'''
		while( len( self.commandQueue ) != 0 ):
			print 'triaiter'
			command = self.commandQueue.pop()
			self.mode[ command[0] ]( command[1:] )
			command.pop()
		'''

	#////////
	# Modes /
	#////////

	# Permet de créer une fenêtre
	# -?-
	# [string] Command:		Commande à effectuer
	# -!-
	# [Manager.STATUSCODE]:	Rapport de déroulement ]
	def MODE_CreateWindow( self, command, testOnly = False ):
		print 'disp ok'

		commandCount = len( command )

		# Nombre de fenêtre à ajouter
		if( commandCount == 0 ):
			windowCount = 1
		elif( strIsInt( command[ 0 ] ) ):
			windowCount = int( command[ 0 ] )

		# Image
		if( commandCount < 2  ):
			imageID = -1
		elif( strIsInt( command[1] ) ):
			imageID = command[ 1 ]

		# Randomize positions
		if( commandCount < 3 ):
			randomizePosition = True
		elif( strIsInt( command[2] ) ):
			randomizePosition = bool( command[ 2 ] )

		if( testOnly ):
			return True
		else:
			# Création des élements
			for windowID in xrange( 0, windowCount ):
				window = BaseWindow()
				window.setRandomPosition( randomizePosition )

				self.windowList.append( window )

			return True

#///////////////////////
# Elements affichables /
#///////////////////////
class BaseWindow( Toplevel ):
	def __init__( self ):
		Toplevel.__init__( self )
		self.title( ' ' )
		self.configure( background='green' )
		self.resizable( width=False, height=False )

		self.__config = {
			'randomPosition': False
		}

	def setRandomPosition( self, state ):
		self.__config__['randomPosition'] = state

		if self.__config__['randomPosition']:
			self.after( CONFIG['WINDOWS_POSUPDATEINTERVAL'], self.randomPosition )

	def setPosition( self, x, y ):
		self.geometry( "%dx%d+%d+%d" % ( self.winfo_width(), self.winfo_height(), x, y ) )

	def randomPosition( self ):
		x = random.randrange( 0, self.winfo_screenwidth() - self.winfo_width() )
		y = random.randrange( 0, self.winfo_screenheight() - self.winfo_height() )

		self.setPosition( x, y )

		if self.__config__['randomPosition']:
			self.after( CONFIG['WINDOWS_POSUPDATEINTERVAL'], self.randomPosition )

#-------------------
# Gère une fenêtre -
#-------------------
"""
class Window( Toplevel ):
	def __init__( self, imageBank ):
		Toplevel.__init__( self )
		self.title( " " )
		self.configure( background="green" )
		self.resizable( width=False, height=False )

		# Chargement de l'image
		image = imageBank.getRandomImage()
		self.canvas = Canvas( self, width=image['width'], height=image['height'] )
		self.canvas.create_image( 0, 0, anchor=NW, image=image['photoimage'] )
		self.canvas.pack()
		self.withdraw()

		self.after( CONFIG['WINDOWS_POSUPDATEINTERVAL'], self.randomPosition )

	def setPosition( self, x, y ):
		self.geometry( "%dx%d+%d+%d" % ( self.winfo_width(), self.winfo_height(), x, y ) )

"""

class ImageWindow( BaseWindow ):
	def __init__( self, imageBank ):
		BaseWindow.__init__( self )

		# Chargement de l'image
		'''
		image = imageBank.getRandomImage()
		self.canvas = Canvas( self, width=image['width'], height=image['height'] )
		self.canvas.create_image( 0, 0, anchor=NW, image=image['photoimage'] )
		self.canvas.pack()
		'''
		#self.withdraw()
