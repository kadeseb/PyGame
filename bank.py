#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Gère les banques de ressources
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ----------------------------------------
import os
import pygame.mixer as Mixer
import PIL.Image
import PIL.ImageTk
from config import *

#----------------
# Gère les sons -
#----------------
class SoundBank():
	##
	# Constructeur
	##
	def __init__( self ):
		self.soundList = os.listdir( CONFIG['SOUNDS_DIR'] )
	##
	# Joue un son
	# -?-
	# [int] id 	Index du son à jouer
	# -!-
	# [bool]	Le son a été joué correctement  	
	##
	def play( self, id ):
		if id >= len( self.soundList ):
			return False

		Mixer.music.load( CONFIG['SOUNDS_DIR'] + self.soundList[ id ] )
		Mixer.music.play()

		return True

	##
	# Retourne la liste des sons
	# -!-
	# [list]	Liste des sons
	##
	def getList( self ):
		return self.soundList

	def exist( self, id ):
		return id < len( self.soundList )

	def action( self ):
		if( not Mixer.music.get_busy() ):
			index = random.randrange( 0, len( self.soundList )  )

			Mixer.music.load( CONFIG['SOUNDS_DIR'] + self.soundList[ index ] )
			Mixer.music.play()

#--------------------
# Gère les images -
#--------------------
class ImageBank():
	##
	# Constructeur
	##
	def __init__( self ):
		imageNameList = os.listdir( CONFIG['IMAGES_DIR'] )

		if( len( imageNameList ) > CONFIG['WINDOWS_NUMBER'] ):
			limit = CONFIG['WINDOWS_NUMBER']
		else:
			limit = len( imageNameList )

		limit = len( imageNameList )

		self.imageList = []

		for i in xrange( 0, limit ):
			image = PIL.Image.open( CONFIG['IMAGES_DIR'] + imageNameList[i] )

			container = {
				'width': image.size[0],
				'height': image.size[1],
				'image': image,
				'photoimage': PIL.ImageTk.PhotoImage( image )
			}

			self.imageList.append( container )

	##
	# Retourne une image aléatoire
	# -!-
	#  [dict]
	##
	def getRandomImage( self ):
		index = random.randrange( 0, len( self.imageList ) )

		return self.imageList[ index ]
