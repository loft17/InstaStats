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



# VERSION
# ##########################################################################################################################
def DetailsLastPost():
    profile = instaloader.Profile.from_username(L.context, PROFILE)
    NumImange = 0
    URL_IMGINS="https://www.instagram.com/p/"

    # 2021-11-30 18:27:27
    #  ID_IMG - POSTED ON - CAPTION - Likes - Comments
    print("Nº\t URL\t Posted on\t Likes\t Comentarios")


    # Conseguimos todos los likes de las ultimas 10 imagenes
    for post in profile.get_posts():
        likes = "0"
        if(NumImange == 2):
            break
        else:
            # Añadimos 1 al contador de imagenes
            NumImange = NumImange + 1

            #print(NumImange, "\t", 
            #    datetime.strptime(str(post.date_utc), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y"),"\t", 
            #    post.likes, "\t", 
            #    post.comments)

            print(NumImange, "\t", URL_IMGINS,post.shortcode)

    #print("obteniendo foloweXs")
    # Obteniendo seguidores del perfil
    #followees = set(profile.get_followees())

    # Mostramos la gente que no hizo like
    #ghosts = followees - likes
    #print("\n" + color.OKGREEN + "Mostramos los followees fantasmas:" + color.ENDC)
    #for ghost in ghosts:
    #    print(ghost.username)