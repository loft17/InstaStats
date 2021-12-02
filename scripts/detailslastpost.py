#!/usr/bin/env python3
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog

import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date, datetime
from configparser import ConfigParser

from scripts import nofollowback, showfollowees, showfollowers, medianumcomments, medianumlikes, totalnumfollowees, resumeninfoaccount, totalnumfollowers, showengagementBBDD, totalnumpost, totalnumcomments, totalnumlikes, detailslastpost


# ------------------------------------------------------------------------------------------------------------------------
# Variales
# ------------------------------------------------------------------------------------------------------------------------
today = date.today()
args = aux_funcs.get_args()
statusvar = "0"

# Fichero de configuracion.
config = ConfigParser()
config.read("config.ini")

NumImangeConf = str(config.get('NUM_CHECK_IMG', 'NumImangeConf'))

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
# EJECUCION
# ##########################################################################################################################
def DetailsLastPost():
    profile = instaloader.Profile.from_username(L.context, PROFILE)
    NumImange = 0
    URL_IMGINS="https://www.instagram.com/p/"

    # 2021-11-30 18:27:27
    #  ID_IMG - POSTED ON - CAPTION - Likes - Comments
    print("\nNº\t URL\t\t\t\t\t\t Posted on\t Likes\t Comentarios\t Engadment")

    # ----------------------------------------------------------------------------------------------------------------------
    # Conseguimos el Engagement, likes, coments, post actual y lo guardamos en la base de datos
    # ----------------------------------------------------------------------------------------------------------------------
    num_followers = profile.followers

    # Conseguimos todos los likes de las ultimas 10 imagenes
    for post in profile.get_posts():
        likes = "0"
        if(NumImange == 10):
            break
        else:
            # Añadimos 1 al contador de imagenes
            NumImange = NumImange + 1
            engagement = round((float(post.likes + post.comments) / num_followers * 100), 2)
            
            print(NumImange, "\t",
                URL_IMGINS+post.shortcode, "\t",
                datetime.strptime(str(post.date_utc), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y"),"\t",
                post.likes, "\t",
                post.comments, "\t", "\t",
                engagement
            )