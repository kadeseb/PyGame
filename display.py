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
	def __init__( self ):
		# Initialisation de TkInter
		self.tk = Tk( )
		self.tk.wm_title(' ')
		self.tk.withdraw()

		# Initialisation de l'object
		self.imageBank = ImageBank()
		self.windowList = []
		self.titleList = [
			'TITLE1',
			'TITLE2',
			'TITLE3'
		]

	# Rafraichi les fenêtres
	def update( self ):
		for windowID in xrange( 0, len( self.windowList ) ):
			self.windowList[ windowID ].update()

	##
	# Permet de créer un fenêtre
	# -?-
	# [dict] configuration:	Configuration de la fenêtre
	# : {
	#	'IMAGE': 		[int]/[None] ID de l'image à afficher
	# 	'RANDOMIZEPOS': 	[bool] Position de la fenêtre aléatoire
	#   'TITLE':		[string]/[None] Nom de la fenêtre / Nom aléatoire
	# }
	##
	def createWindow( self, configuration ):
		window = WindowImage( self.imageBank, configuration )
		self.windowList.append( window )

	# Liste les fenêtres disponibles
	# -!-
	# [list]
	def getWindowList( self, configuration ):
		0

	# Retourn imageBank
	def getImageBank( self ):
		return self.imageBank

#///////////////////////
# Elements affichables /
#///////////////////////
class BaseWindow( Toplevel ):
	def __init__( self ):
		Toplevel.__init__( self )

		# Initialisation
		self._randomizePosition = False
		self._title = ' '
		self.width = 500
		self.height = 500

		# Configuration
		self.title( ' ' )
		self.configure( background='green' )
		self.resizable( width=False, height=False )
		self.randomPosition()

	def setRandomPosition( self, state ):
		self._randomizePosition = bool( state )

		if self._randomizePosition:
			self.after( CONFIG['WINDOWS_POSUPDATEINTERVAL'], self.randomPosition )

	def setPosition( self, x, y ):
		#self.geometry( "%dx%d+%d+%d" % ( self.winfo_width(), self.winfo_height(), x, y ) )
		self.geometry( "%dx%d+%d+%d" % ( self.width, self.height, x, y ) )

	def randomPosition( self ):
		x = random.randrange( 0, self.winfo_screenwidth() - self.winfo_width() )
		y = random.randrange( 0, self.winfo_screenheight() - self.winfo_height() )

		self.setPosition( x, y )

		if self._randomizePosition:
			self.after( CONFIG['WINDOWS_POSUPDATEINTERVAL'], self.randomPosition )

#-------------------
# Gère une fenêtre -
#-------------------
class WindowImage( BaseWindow ):
	def __init__( self, imageBank, configuration ):
		BaseWindow.__init__( self )
		self.applyConfig( configuration, imageBank )

	# : {
	#	'IMAGE': 		[int]/[None] ID de l'image à afficher
	# 	'RANDOMIZE': 	[bool] Position de la fenêtre aléatoire
	#   'TITLE':		[string]/[None] Nom de la fenêtre / Nom aléatoire
	# }
	def applyConfig( self, configuration, imageBank ):
		if( (not 'IMAGE' in configuration) or (not 'RANDOMIZEPOS' in configuration) or (not 'TITLE' in configuration) ):
			return False

		# Intégration de l'image
		if( configuration['IMAGE'] == None ):
			image = imageBank.getRandomImage()
		else:
			image = imageBank.getImage( int( configuration['IMAGE'] ) )

			if( image == None ):
				return False

		self.width, self.height = image['width'], image['height']
		self.geometry( '%dx%d' % (self.width, self.height) )

		self.canvas = Canvas( self, width=self.width, height= self.height )
		self.canvas.create_image( 0, 0, anchor=NW, image=image['photoimage'] )
		self.canvas.pack()

		# Position aléatoire
		self.setRandomPosition( configuration['RANDOMIZEPOS'] )

		# Choix du titre
		if( configuration['TITLE'] == None ):
			#self.wm_title( self.titleList[ random.randrange( 0, len( self.titleList ) ) ] )
			self.wm_title( 'Titre par défault' )
		elif( isinstance( configuration['TITLE'], str ) ):
			self.wm_title( configuration['TITLE'] )
		else:
			return False

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

		self.withdraw()'''
