#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ========================================
# Projet:	PyJoke
# Rôle:		Gère les banques de ressources
# Crée le:	09/10/2016
# ========================================
import os
import PIL.Image
import PIL.ImageTk
import random
from config import *

class ImageBank():
	# Constructeur
	def __init__( self ):
		imageNameList = os.listdir( CONFIG['IMAGES_DIR'] )
		self.imageList = []

		for i in xrange( 0, len( imageNameList ) ):
			image = PIL.Image.open( CONFIG['IMAGES_DIR'] + imageNameList[i] )

			container = {
				'width': image.size[0],
				'height': image.size[1],
				'image': image,
				'photoimage': PIL.ImageTk.PhotoImage( image ),
				'name': imageNameList[i]
			}

			self.imageList.append( container )

	# Retourne une image aléatoire
	#
	# -!-
	# [dict]
	def getRandomImage( self ):
		return self.imageList[ random.randrange( 0, len( self.imageList ) ) ]

	# Retoune un id d'image aléatoire
	#
	# -!-
	# [int]
	def getRandomImageID( self ):
		return random.randrange( 0, len( self.imageList ) )

	# Retourne l'image spécifié
	#
	# -?-
	# [int] imageID:	ID de l'image
	# -!-
	# [dict]
	def getImage( self, imageID ):
		if( self.exist( imageID ) ):
			return self.imageList[ imageID ]
		else:
			return None

	# Vérifie l'existence d'une image
	#
	# -?-
	# [int] imageID:	ID de l'imageID
	# -!-
	# [bool]
	# -$-
	# [TypeError]		! -?-
	def exist( self, imageID ):
		if( not isinstance( imageID, int ) ):
			raise TypeError( '! -?-' )

		try:
			self.imageList[ imageID ]
		except KeyError:
			return False
		return True

	# Retourne la liste des images disponibles
	#
	# -!-
	# [list]
	def getList( self ):
		return self.imageList
