#!/usr/bin/env python3
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog

import os, aux_funcs, argparse, re, menu_ayuda, printcolors
import instaloader
import mysql.connector

from datetime import date
from configparser import ConfigParser


# ------------------------------------------------------------------------------------------------------------------------
# Variales
# ------------------------------------------------------------------------------------------------------------------------
today = date.today()
args = aux_funcs.get_args()
statusvar = "0"

# Fichero de configuracion.
config = ConfigParser()
config.read("config.ini")


# Variables para conectar a Instagram
L = instaloader.Instaloader()
#USER = args.user
#PROFILE = USER
USER = args.login
PROFILE = args.user




L.load_session_from_file(USER)
#profile = instaloader.Profile.from_username(L.context, PROFILE)

# Variables para colorear el texto en consola
color = printcolors.bcolors()

# ##########################################################################################################################
# conexión BBDD
# ##########################################################################################################################
ConnectBBDD=mysql.connector.connect(
	host =      (config.get('MYSQL', 'Server')),
	user =      (config.get('MYSQL', 'Username')),
	passwd =    (config.get('MYSQL', 'Password')),
	database =  (config.get('MYSQL', 'Database'))
)


# ##########################################################################################################################
# Numero MEDIA LIKES por post
# ##########################################################################################################################
def MediaNumLikes():
    ConnectShowMediaLikes=ConnectBBDD.cursor()
    ConnectShowMediaLikes.execute(
        "SELECT total_likes FROM ig_report WHERE date = %s AND account = %s", (today, PROFILE)
    )
    SqlShowMediaNumLikes = (int(*ConnectShowMediaLikes.fetchone()))
    
    ConnectShowMediaLikes.execute(
        "SELECT total_post FROM ig_report WHERE date = %s AND account = %s", (today, PROFILE)
    )
    SqlShowMediaNumPost = (int(*ConnectShowMediaLikes.fetchone()))

    NumMediaLikesPosts = round(SqlShowMediaNumLikes / SqlShowMediaNumPost, 2)
    print("Media Likes por post: " + color.OKGREEN + str(NumMediaLikesPosts) + color.ENDC)
