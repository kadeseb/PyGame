#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Contient toutes les commandes
# Auteur:   kadeseb
# Crée le:	09/10/2016
# ----------------------------------------
from docopt import docopt, DocoptExit
from functions import *
import subprocess
import re

# //////////// #
# Classe mère  #
# //////////// #
class Command:
    _FORMAT_ = 'Usage: $CMD'
    _DESCRIBTION_ = 'Aucune description'
    _CODE_ = {
    	'OK': 0,
    	'BADCMD': 1,
    	'BADARG': 2,
    	'NOTFOUND': 3,
    	'INVALIDCODE': 4,
        'UNKNOW': 5
    }
    _CODE_STATUS_ =  {
    	0: "OK",
    	1: "Commande invalide",
    	2: "Argument incorrect",
    	3: "Element non trouvé",
    	4: "Code invalide"
    }

    def __init__( self, name ):
    	self._FORMAT_ = self._FORMAT_.replace( '$CMD', name )
    	self.code = Command._CODE_[ 'OK' ]
    	self.output = ''

    def __execute__( self, _args_, _ctx_ ):
        try:
            _args_ = docopt( self._FORMAT_, argv=_args_, options_first=True, help=False )
        except DocoptExit:
            self.code = Command._CODE_[ 'BADARG' ]
            self.output = self._FORMAT_
            return

        self.action( _args_, _ctx_ )

    def __result__( self ):
        if( self.code in Command._CODE_STATUS_ ):
            status = Command._CODE_STATUS_[ self.code ]
            code = self.code
        else:
            code = Command._CODE_[ 'INVALIDCODE' ]
            status = Command._CODE_STATUS_[ code ]

        return {
            'CODE': code,
            'STATUS': status,
            'OUTPUT': self.output
        }

    def setCode( self, vcode ):
        try:
            self.code = Command._CODE_[ vcode ]
        except KeyError:
            self.code = Command._CODE_[ 'INVALIDCODE' ]

    def addOutput( self, content, end="\n" ):
        self.output += content + end

    def addIOutput( self, content ):
        self.addOutput( content, end='' )

    def action( self, commandManager ):
    	print 'OK'

    # Retourne une instance de la classe spécifié
    #
    # -?-
    # [~Command] / [None]
    def _getObjectFromClassName( self, className, commandName ):
        if( not re.match( '^\w+$', className ) ):
            return None

        try:
            return eval( className + '( "%s" )' % commandName )
        except NameError:
            print 'name error'
            return None

    # Reoune la description
    #
    # -?-
    # [str]
    def _getDescribtion( self ):
        return self._DESCRIBTION_

    # Retourne l'usage d'une commande:
    #
    # -?-
    # [str]
    def _getFormat( self ):
        return self._FORMAT_

# //////////// #

# ==
# Rôle:     Déconnecte le client
# Crée le:  01/12/2016
# ==
class Command_Exit( Command ):
    _DESCRIBTION_ = 'Déconnecte le client'

    def action( self, _args_, _ctx_):
    	self.addIOutput( 'Vous allez être déconnecté !' )
        self.setCode( 'OK' )

# ==
# Rôle:     Arrête le serveur
# Crée le:  19/09/2016
# ==
class Command_Quit( Command ):
    _DESCRIBTION_ = 'Quitte le programme'

    def action( self, _args_, _ctx_):
        _ctx_['EXITING'] = True
    	self.addIOutput( 'Arrêt du serveur' )
        self.setCode( 'OK' )

# ==
# Rôle:     Affiche l'aide
# Crée le:  19/09/2016
# ==
class Command_Help( Command ):
    _DESCRIBTION_ = 'Affiche l\'aide'
    _FORMAT_ =  'Usage: $CMD [<command>]'

    def action( self, _args_, _ctx_ ):
        if( _args_['<command>'] ):
            self.commandUsage( _args_['<command>'], _ctx_ )
        else:
            self.listCommand( _ctx_ )

    # Affiche la façpon du(iliser une commande)
    #
    # -?-
    # [str] command:    Command
    def commandUsage( self, command, _ctx_ ):
        try:
            commandClass = _ctx_['COMMAND'][ command ]
        except KeyError:
            self.setCode( 'BADARG' )
            return

        commandName = command
        commandObject = self._getObjectFromClassName( commandClass, commandName )

        self.addOutput( commandObject._getDescribtion() )
        self.addOutput( '' )
        self.addOutput( commandObject._getFormat() )
        self.setCode( 'OK' )

    # Affiche la liste des commandes#
    # -?-
    # [dict] _ctx_:     Contexte d'exécution
    def listCommand( self, _ctx_ ):
        self.addOutput( 'Tappez "help [<command>]" pour obtenir l\'aide détaillée d\'une commande' )
        self.addOutput( '' )
        self.addOutput( '[Commande]\t[Description]' )

        commandList = _ctx_['COMMAND'].keys()

        for i in xrange( 0, len( _ctx_['COMMAND'] ) ):
            className = _ctx_['COMMAND'][ commandList[ i ] ]
            command = commandList[ i ]
            commandObject = self._getObjectFromClassName( className, command )

            self.addOutput( '%s\t%s' % ( command, commandObject._getDescribtion() ) )

        self.setCode( 'OK' )

# ===
# Rôle:     Permet d'éjecter le lecteur CD
# Crée le:  15/10/2016
# ===
class Command_Eject( Command ):
    _DESCRIBTION_ = 'Ouvre le lecteur CD'

    def action( self, _args_, _ctx_ ):
        subprocess.Popen( 'eject' )
        self.addIOutput( 'Lecteur CD ouvert'  )
        self.setCode( 'OK' )

# ===
# Rôle:     Permet de jouer des sons
# Crée le:  15/10/2016
# ===
class Command_Sound( Command ):
    _FORMAT_ = 	'Usage:\n'
    _FORMAT_ += '	$CMD list\n'
    _FORMAT_ += '	$CMD play <id> [<count>] [<delais>]\n'
    _FORMAT_ += '	$CMD purge'

    _DESCRIBTION_ = "Gère les sons"

    def action( self, _args_, _ctx_ ):
        self.soundManager = _ctx_['SOUND']

        if( _args_['list'] ):
            self.list()
        elif( _args_['play'] ):
            self.play( _args_ )
        elif( _args_['purge'] ):
            self.purge()

    # Sort la liste des sons
    def list( self ):
        soundList = self.soundManager.getSoundList()

        self.output += 'Liste des sons:\n'
        self.output += '[ID]\t[Fichier]'

        for soundID in xrange( 0, len( soundList ) ):
            self.output += '\n%d\t\t%s' % ( soundID, soundList[ soundID ] )

        self.code = Command._CODE_['OK']

    # Joue un son
    #
    # -?-
    # [dict] _args_
    # [sound.Manager] soundManager: Gestionnaires de sons
    def play( self, _args_ ):
        # ID du son
        if( not self.soundManager.validSound( _args_['<id>'] ) ):
            self.code = Command._CODE_['NOTFOUND']
            self.output = 'Le son spécifié n\'existe pas !'
            return
        else:
            soundID = int( _args_['<id>'] )

        # Nombre de lecture
        if( _args_['<count>'] ):
            if( strIsInt( _args_['<count>'] ) ):
                count = int( _args_['<count>'] )
            else:
                self.code = Command._CODE_['BADARG']
                return
        else:
            count = 1

        # Delais
        if( _args_['<delais>'] ):
            if( strIsInt( _args_['<delais>'] ) ):
                delais = int( _args_['<delais>'] )
            else:
                self.code = Command._CODE_['BADARG']
                return
        else:
            delais = 0

        for i in xrange( 0, count ):
            self.soundManager.playlistAdd( soundID, delais )

        self.code = Command._CODE_['OK']

    # Purge un son
    #
    # -?-
    # [sound.Manager] soundManager: Gestionnaires de sons
    def purge( self ):
        self.soundManager.playlistPurge()
        self.code = Command._CODE_['OK']

# ==
# Rôle:     Gère l'affichage de fenêtre
# Crée le:  16/09/2016
# ==
class Command_Window( Command ):
    _FORMAT_ = 	'Usage: \n'
    _FORMAT_ += '	$CMD list (image | window)            Liste les fenêtres ou images\n'
    _FORMAT_ += '	$CMD create [options] [<count>]       Ouvre une fenêtre\n'
    _FORMAT_ += '	$CMD set [options] <windowID>...      Change les propriétés d\'une fenêtre\n'
    _FORMAT_ += '	$CMD close [all | (<windowID>...)]    Fermeture de fenêtre\n'
    _FORMAT_ += '\n'
    _FORMAT_ += 'Options:\n'
    _FORMAT_ += '-r=(1 | 0) --randomizePosition=(1 | 0)	  Position de la fenêtre aléatoire\n'
    _FORMAT_ += '-i=IMAGE --image=IMAGE 		          Image de la fenêtre\n'
    _FORMAT_ += '-t=TITLE --title=TITLE 		          Titre de la fenêtre'

    _DESCRIBTION_ = "Gère l\'afichage de fenêtre"

    def action( self, _args_, _ctx_ ):
    	# Liste des images/fenêtre
    	if( _args_['list'] ):
    		if( _args_['image'] ):
    			self.listImage( _ctx_['DISPLAY'] )
    		elif( _args_['window'] ):
    			self.listWindow( _ctx_['DISPLAY'] )
    	elif( _args_['create'] ):
    		self.create( _args_, _ctx_['DISPLAY'] )
    	elif( _args_['set'] ):
    		self.set( _args_, _ctx_['DISPLAY'] )
    	elif( _args_['close'] ):
    		self.close( _args_, _ctx_['DISPLAY'] )

    # Liste les images disponibles
    #
    # -?-
    # [display.Manager] displayManage:  Gestionnaires de fenêtres
    def listImage( self, displayManager ):
    	imageList = displayManager.getImageBank().getList()

    	self.output += 'Liste des images:\n'
    	self.output += '[ID]\t[Taille]\t[Nom]'

    	for imageID in xrange( 0, len( imageList ) ):
    		size = '%dx%d' % ( imageList[imageID]['width'], imageList[imageID]['height'] )
    		name = imageList[imageID]['name']

    		self.output += '\n%d\t\t%s\t\t%s' % ( imageID, size, name  )

    	self.code = Command._CODE_['OK']

    # Liste les fenêtres ouvertes
    # -?-
    # [display.Manager] displayManage:  Gestionnaires de fenêtres
    def listWindow( self, displayManager ):
    	self.output += 'Liste des fenêtres:\n'
    	self.output += '[ID]\t[RandPos]\t[Image]\t'

    	for windowID in displayManager.getWindowIDList():
    		window = displayManager.getWindow( windowID )

    		self.output += '\n %d\t\t %d\t\t %s' % ( windowID, window.getRandomPosition() ,window.getImageName() )

    	self.code = Command._CODE_['OK']

    # Créer une fenêtre
    #
    # -?-
    # [dict] _args_
    # [display.Manager] displayManager
    def create( self, _args_, displayManager ):
    	config = displayManager.createConfig( _args_['--image'], _args_['--randomizePosition'], _args_['--title'] )

    	if( config == None ):
    		self.code = Command._CODE_['BADARG']
    		return

    	if( _args_['<count>'] ):
    		if( strIsInt( _args_['<count>'] ) ):
    			windowCount = int( _args_['<count>'] )
    		else:
    			self.code = Command._CODE_['BADARG']
    			return
    	else:
    		windowCount = 1

    	for i in xrange( 0, windowCount ):
    		displayManager.createWindow( config )

    # Edite les propriétés d'une fenêtre
    def set( self, _args_, displayManager ):
    	config = displayManager.createConfig( _args_['--image'], _args_['--randomizePosition'], _args_['--title'] )
    	valid = 0

    	for windowID in _args_['<windowID>']:
    		if( not strIsInt( windowID ) or not displayManager.windowIDExist( int( windowID ) ) ):
    			continue

    		window = displayManager.getWindow( int( windowID ) )

    		if( _args_['--image'] != None ):
    			window.setImage( config['IMAGE'] )

    		if( _args_['--randomizePosition'] != None ):
    			window.setRandomPosition( config['RANDOMIZEPOS'] )

    		if( _args_['--title'] != None ):
    			window.setTitle( config['TITLE'] )

    		valid += 1

    	if not valid:
    		self.code = Command._CODE_['BADARG']
    		self.output += 'Aucunes des fenêtres n\'existe !'
    	else:
    		self.code = Command._CODE_['OK']
    		self.output += 'Changement appliquée(s)'

    		if( valid < len( _args_['<windowID>'] ) ):
    			self.output += ', à l\'exception des fenêtres inexistantes'

    def close( self, _args_, displayManager ):
    	windowList = displayManager.getWindowIDList() if( _args_['all'] ) else _args_['<windowID>']
    	valid = 0

    	for windowID in windowList:
    		if strIsInt( windowID ) and displayManager.closeWindow( int( windowID ) ):
    			valid += 1

    	if( not valid ):
    		self.code = Command._CODE_['BADARG']
    	else:
    		self.code = Command._CODE_['OK']
    		self.output += 'Fermeture effectuée(s)'

    		if( valid < len( _args_['<windowID>'] ) ):
    			self.output += ', à l\'exception des fenêtres inexistantes'
