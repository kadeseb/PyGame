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
	# Constructeur
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
			if( self.windowList[ windowID ] == None ):
				continue

			self.windowList[ windowID ].update()

			if( self.windowList[ windowID ].getClosed() ):
				self.windowList[ windowID ] = None;

	# Permet de créer un fenêtre
	#
	# -?-
	# [dict] config:	Configuration de la fenêtre
	# : {
	#	'IMAGE': 		[int]/[None] ID de l'image à afficher
	# 	'RANDOMIZEPOS': 	[bool] Position de la fenêtre aléatoire
	#   'TITLE':		[string]/[None] Nom de la fenêtre / Nom aléatoire
	# }
	def createWindow( self, config ):
		if( not self.validConfig( config ) ):
			return False

		window = WindowImage( self.imageBank )

		window.setTitle( config['TITLE'] )
		window.setImage( config['IMAGE'] )
		window.setRandomPosition( config['RANDOMIZEPOS'] )

		self.windowList.append( window )

		return True

	# Ferme une fenêtre
	#
	# -?-
	# [int] windowID 	Identifiant de la fenêtre à fermer
	# -!-
	# [bool]
	def closeWindow( self, windowID ):
		if( not self.windowIDExist( windowID ) or self.windowList[ windowID ] == None ):
			return False

		self.windowList[ windowID ].destroy()
		self.windowList[ windowID ].setClosed( True )

		return True


	# Liste les fenêtres disponibles
	#
	# -!-
	# [list]
	def getWindowIDList( self ):
		IDList = []

		for i in xrange( 0, len( self.windowList ) ):
			if( self.windowList[i] != None ):
				IDList.append( i )

		return IDList

	def getWindow( self, windowID ):
		try:
			return self.windowList[ windowID ]
		except KeyError:
			return None

	# Contrôle l'existance d'une fenêtre
	def windowIDExist( self, windowID ):
		try:
			self.windowList[ windowID ]
		except:
			return False

		return True

	# Contrôle la validité de la configuration
	#
	# -?-
	# [dict] configuration
	# -!-
	# [bool] La configuration est valide
	@staticmethod
	def validConfig( configuration ):
		try:
			configuration['IMAGE']
			configuration['RANDOMIZEPOS']
			configuration['TITLE']
		except KeyError:
			return False

		if( not isinstance( configuration['IMAGE'], int ) ):
			return False
		elif( not isinstance( configuration['RANDOMIZEPOS'], bool ) ):
			return False
		elif( not isinstance( configuration['TITLE'], str ) ):
			return False

		return True

	# Extrait une configuration
	#
	# -?-
	# imageID
	# randomizePos
	# title
	# -!-
	# [dict] / [None]
	def createConfig( self, imageID, randomizePos, title ):
		# Extraction de l'image
		if( imageID == None ):
			imageID = self.imageBank.getRandomImageID()
		elif( strIsInt( imageID ) and self.imageBank.exist( int( imageID ) ) ):
			imageID = int( imageID )
		else:
			return None

		# Position aléatoire
		if( randomizePos == None ):
			randomizePos = True
		elif( strIsInt( randomizePos ) ):
			randomizePos = bool( int( randomizePos ) )

		# Titre
		if( title == None ):
			title = 'Titre par défault'
		elif( not isinstance( title, str ) ):
			try:
				title = str( title )
			except:
				return None

		return {
			'IMAGE': imageID,
			'RANDOMIZEPOS': randomizePos,
			'TITLE': title
		}

	def getImageBank( self ):
		return self.imageBank



#///////////////////////
# Elements affichables /
#///////////////////////
class BaseWindow( Toplevel ):
	# Constructeur
	def __init__( self ):
		Toplevel.__init__( self )

		# Initialisation
		self._randomizePosition = False
		self._title = ' '
		self.width = 500
		self.height = 500
		self.closed = False

		# Configuration
		self.title( ' ' )
		self.configure( background='green' )
		self.resizable( width=False, height=False )
		self.randomPosition()

	# Définit l'état des déplacements aléatoires
	#
	# -?-
	# [bool] state
	def setRandomPosition( self, state ):
		self._randomizePosition = bool( state )

		if self._randomizePosition:
			self.after( CONFIG['WINDOWS_POSUPDATEINTERVAL'], self.randomPosition )

	# Retourne l'état de randomPosition
	#
	# -!-
	# [bool]
	def getRandomPosition( self ):
		return self._randomizePosition

	# Change la position de la fenêtre:
	#
	# -?-
	# [int] x	Position x
	# [int] y	Position y
	def setPosition( self, x, y ):
		#self.geometry( "%dx%d+%d+%d" % ( self.winfo_width(), self.winfo_height(), x, y ) )
		self.geometry( "%dx%d+%d+%d" % ( self.width, self.height, x, y ) )

	# Déplace la fenêtre à une position aléatoire
	def randomPosition( self ):
		x = random.randrange( 0, self.winfo_screenwidth() - self.winfo_width() )
		y = random.randrange( 0, self.winfo_screenheight() - self.winfo_height() )

		self.setPosition( x, y )

		if self._randomizePosition:
			self.after( CONFIG['WINDOWS_POSUPDATEINTERVAL'], self.randomPosition )

	# Change le titre de la fenêtre
	#
	# -?-
	# [str] title	Titre de la fenêtre
	# -!-
	# [bool]
	def setTitle( self, title ):
		if( not isinstance( title, str ) ):
			return False

		self.title( title )
		return True

	# Retourne le titre de la fenêtre
	#
	# -!-
	# [str]
	def getTitle( self ):
		return self.wm_title()

	# Retourne l'état de la fenêtre
	def getClosed( self ):
		return self.closed

	# Change l'état de fermeture de la fenêtre
	def setClosed( self, value ):
		self.closed = value
#-------------------
# Gère une fenêtre -
#-------------------
class WindowImage( BaseWindow ):
	# Constructeur
	# -?-
	# [BankImage] Banque d'image
	def __init__( self, bankImage ):
		BaseWindow.__init__( self )

		self.imageBank = bankImage
		self.canvas = None
		self._image = 0

	# Définit l'image de la fenêtre
	#
	# -?-
	# [int] imageID:			ID l'image à intégrer
	# -!-
	# [bool]
	def setImage( self, imageID ):
		if( not isinstance( imageID, int) or not self.imageBank.exist( imageID ) ):
			return False

		image = self.imageBank.getImage( imageID )
		self._image = image
		self.width, self.height = image['width'], image['height']
		self.geometry( '%dx%d' % (self.width, self.height) )

		if( self.canvas != None ):
			#self.pack_forget()
			self.canvas.destroy()

		self.canvas = Canvas( self, width=self.width, height=self.height )
		self.canvas.create_image( 0, 0, anchor=NW, image=image['photoimage'] )
		self.canvas.pack()

	# Retourne l'image selectionné:
	def getImageName( self ):
		return self._image['name']
