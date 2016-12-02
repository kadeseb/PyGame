#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ========================================
# Projet:	PyJoke
# Rôle:		Gère le volume audio
# Crée le:	01/12/2016
# ========================================
import subprocess

class Volume:
	def __init__( self ):
		soundCards = Volume._getSoundCards()

		# Récupération des mixers
		for soundCard in soundCards:
			self.mixers = Volume._getMixers( soundCard )

		# Identification des mixers utiles
		self.usefullMixers = list()

		for mixerName, mixerInfo in self.mixers.iteritems():
			for key,value in mixerInfo.iteritems():
				if( key == 'Capabilities' and value == 'pvolume pvolume-joined pswitch pswitch-joined'):
					self.usefullMixers.append( mixerName )

	# Met le volume au maximum et active les mixers
	def maximize( self ):
		for mixer in self.usefullMixers:
				Volume._setMixer( mixer, 100, True )

	# Retourne la liste des cartes son disponibles
	#
	# -!-
	# [list]
	@staticmethod
	def _getSoundCards():
		soundCards = list()
		rawInfo = subprocess.check_output( ["aplay", "-l"] ).split('\n')[:-1]

		for indice in xrange( 1, len( rawInfo ) ):
			line = rawInfo[indice]

			if( line[0] != ' ' ):
				delimiter = line.find(':')

				cardID = line[ 6: delimiter ]
				cardName = line[ delimiter+1: line.find( ',', delimiter+1 ) ]

				if( not cardID in soundCards ):
					soundCards.append( int( cardID ) )

		return soundCards

	# Retourne la liste des mixers
	#
	# [int] soundCard:	Carte son
	# -!-
	# [dict]
	@staticmethod
	def _getMixers( soundCard ):
		if( not isinstance( soundCard, int ) ):
			raise TypeError( '<soundCard> n\'est pas de type [int] !' )

		rawInfo = subprocess.check_output( ['amixer', '-c' + str( soundCard ) ] ).split('\n')[:-1]
		mixers = dict()

		for line in rawInfo:
			if( line[0] != ' ' ):
				mixerName = line[ 22 : line.find( '\'', 22) ]

				mixers[ mixerName ] = dict()
			else:
				delimiter = line.find( ':' )

				key = line[ 2 : delimiter ]
				value = line[ delimiter+2 : len( line ) ]

				mixers[ mixerName ][ key ] = value

		mixers.pop( 'Beep' )

		return mixers

	@staticmethod
	def _setMixer( mixer, volume, on ):
		subprocess.check_output( ['amixer', 'sset', '\'' + str( mixer ) + '\'', str( volume ) + '%'] )
		subprocess.check_output( ['amixer', 'sset', '\'' + str( mixer ) + '\'', 'on' if on else 'off' ] )
