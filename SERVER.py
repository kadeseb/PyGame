#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ----------------------------------------
import os
import pygame.mixer as Mixer
# ---
import config
import network as Network
import action

##################
# Initialisation #
##################
# Pygame Mixer
Mixer.init()
print '***********************'
print '* PyBlague Serveur v1 *'
print '***********************'
manager = action.Manager()
server = Network.Server( manager )
server.start()

while not manager.askExit():
	manager.action()
