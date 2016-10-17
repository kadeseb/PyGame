#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Gère les banques de ressources
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ----------------------------------------
import os
import PIL.Image
import PIL.ImageTk
import random
from config import *

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
				'photoimage': PIL.ImageTk.PhotoImage( image ),
				'name': imageNameList[i]
			}

			self.imageList.append( container )

	##
	# Retourne une image aléatoire
	# -!-
	# [dict]
	##
	def getRandomImage( self ):
		index = random.randrange( 0, len( self.imageList ) )

		return self.imageList[ index ]

	def getRandomImageID( self ):
		return random.randrange( 0, len( self.imageList ) )

	##
	# Retourne l'image spécifié
	# -?-
	# [int] imageID:	ID de l'image
	# -!-
	# [dict]
	##
	def getImage( self, imageID ):
		if( self.exist( imageID ) ):
			return self.imageList[ imageID ]
		else:
			return None

	##
	# Vérifie l'existence d'une image
	# -?-
	# [int] imageID:	ID de l'imageID
	# -!-
	# [bool]
	##
	def exist( self, imageID ):
		try:
			self.imageList[ imageID ]
		except KeyError:
			return False
		return True

	##
	# Retourne la liste des images disponibles
	# -!-
	# [list]
	##
	def getList( self ):
		return self.imageList
