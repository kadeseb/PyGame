#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ========================================
# Projet:	PyJoke
# Rôle:		Lance le serveur PyJoke
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ========================================
if __name__ == '__main__':
	print '======================'
	print '= PyJoke Server [v2] ='
	print '======================'

	import network as Network
	import command as Command

	############################
	# Gestionnaire de commande #
	############################
	manager = Command.Manager()

	###########
	# Serveur #
	###########
	server = Network.Server( manager )
	server.start()

	manager.run()
