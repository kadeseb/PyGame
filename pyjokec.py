#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Programme client
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ----------------------------------------
import sys
import network as Network
from docopt import docopt
from functions import *
from config import *

format = '''
Usage:
	CLIENT.py <serveur> [<port>]

Options:
	--help					Affiche ce message et quite le programme
'''

if __name__ == '__main__':
	print '======================'
	print '= PyJoke Client v1.2 ='
	print '======================'

	arguments = docopt( format, version='PyJoke Client 1.0', options_first=False )
	hostname = arguments['<serveur>']
	port = arguments['<port>']

	if( port ):
		if( portIsValid( port ) ):
			port = int( port )
		else:
			print '-> [Erreur] Port invalide !'
			exit( 1 )
	else:
		port = CONFIG['PORT']

	#/////////////////////////
	# Execution du programme /
	#/////////////////////////
	print '-> Connexion à %s:%d' % ( hostname, port )

	session = Network.ClientSession()
	connected = session.connect( hostname, port )

	if( not connected ):
		print '-> [ERREUR]: Connection refusé !'
		exit( 1 )
	else:
		print '-> Connecté !\n%s' % ( '='*22 )

	while True:
		try:
			command = raw_input( '#> ' )
			response = session.sendCommand( command )
			print '| Status:', response['STATUS']
			print '| ' + '-'*60

			for line in response['OUTPUT'].split( '\n' ):
				print '| ', line

		except KeyboardInterrupt:
			print 'Stop'
			exit( 0 )
