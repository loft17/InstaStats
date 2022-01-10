import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date, datetime
from configparser import ConfigParser

# ------------------------------------------------------------------------------------------------------------------------
# Variales
# ------------------------------------------------------------------------------------------------------------------------
today = date.today()

args = aux_funcs.get_args()


# Fichero de configuracion.
config = ConfigParser()
config.read("config.ini")


# Variables para colorear el texto en consola
color = printcolors.bcolors()


# ##########################################################################################################################
# GHOST LAST IMG FOLLOWERS
# ##########################################################################################################################
def LastFollowers():
    
    # Variables para conectar a Instagram
    L = instaloader.Instaloader()
    L.load_session_from_file(args.login)
    profile = instaloader.Profile.from_username(L.context, args.user)

    NumImange = 0
    likes = set()

    # Conseguimos todos los likes de las ultimas 10 imagenes
    for post in profile.get_posts():
        if(NumImange == 10):
            break
        else:
            likes = likes | set(post.get_likes())
            NumImange = NumImange + 1

    # Obteniendo seguidores del perfil
    followers = set(profile.get_followers())

    # Mostramos la gente que no hizo like
    ghosts = followers - likes
    print("\n" + color.OKGREEN + "Mostramos los followers fantasmas:" + color.ENDC)
    for ghost in ghosts:
        print(ghost.username)



# ##########################################################################################################################
# GHOST LAST IMG FOLLOWEES
# ##########################################################################################################################
def LastFollowees():
    # Variables para conectar a Instagram
    L = instaloader.Instaloader()
    L.load_session_from_file(args.login)
    profile = instaloader.Profile.from_username(L.context, args.user)
    NumImange = 0
    likes = set()

    #print("sacamos los likes")
    # Conseguimos todos los likes de las ultimas 10 imagenes
    for post in profile.get_posts():
        if(NumImange == 5):
            break
        else:
            likes = likes | set(post.get_likes())
            NumImange = NumImange + 1

    #print("obteniendo foloweXs")
    # Obteniendo seguidores del perfil
    followees = set(profile.get_followees())

    # Mostramos la gente que no hizo like
    ghosts = followees - likes
    print("\n" + color.OKGREEN + "Mostramos los followees fantasmas:" + color.ENDC)
    for ghost in ghosts:
        print(ghost.username)



# ##########################################################################################################################
# GHOST IMG FOLLOWERS
# ##########################################################################################################################
def TotalFollowers():
    # Variables para conectar a Instagram
    L = instaloader.Instaloader()
    L.load_session_from_file(args.login)
    profile = instaloader.Profile.from_username(L.context, args.user)
    NumImange = 0
    likes = set()

    # Conseguimos todos los likes de las ultimas 10 imagenes
    for post in profile.get_posts():
            likes = likes | set(post.get_likes())

    # Obteniendo seguidores del perfil
    followers = set(profile.get_followers())

    # Mostramos la gente que no hizo like
    ghosts = followers - likes
    print("\n" + color.OKGREEN + "Mostramos los followers fantasmas:" + color.ENDC)
    for ghost in ghosts:
        print(ghost.username)



# ##########################################################################################################################
# GHOST FOLLOWEES
# ##########################################################################################################################
def TotalFollowees():
    # Variables para conectar a Instagram
    L = instaloader.Instaloader()
    L.load_session_from_file(args.login)
    profile = instaloader.Profile.from_username(L.context, args.user)
    
    NumImange = 0
    likes = set()

    #print("sacamos los likes")
    # Conseguimos todos los likes de las ultimas 10 imagenes
    for post in profile.get_posts():
        if(NumImange == 10):
            likes = likes | set(post.get_likes())

    #print("obteniendo foloweXs")
    # Obteniendo seguidores del perfil
    followees = set(profile.get_followees())

    # Mostramos la gente que no hizo like
    ghosts = followees - likes
    print("\n" + color.OKGREEN + "Mostramos los followees fantasmas:" + color.ENDC)
    for ghost in ghosts:
        print(ghost.username)



# ##########################################################################################################################
# GHOST LAST IMG FOLLOWEES
# ##########################################################################################################################
def LastFolloweesExt():
    # Variables para conectar a Instagram
    L = instaloader.Instaloader()
    L.load_session_from_file(args.login)
    profile = instaloader.Profile.from_username(L.context, args.user)
    NumImange = 0
    likes = set()

    #print("sacamos los likes")
    # Conseguimos todos los likes de las ultimas 10 imagenes
    for post in profile.get_posts():
        if(NumImange == 5):
            break
        else:
            likes = likes | set(post.get_likes())
            NumImange = NumImange + 1

    #print("obteniendo foloweXs")
    # Obteniendo seguidores del perfil
    followees = set(profile.get_followees())

    # Mostramos la gente que no hizo like
    ghosts = followees - likes
    print("\n" + color.OKGREEN + "Mostramos los followees que no dieron like en las ultimas 5 fotos:" + color.ENDC)
    
    for ghost in ghosts:
            profile = instaloader.Profile.from_username(L.context, str(ghost.username))
            NumImange = 0

            for post in profile.get_posts():
                if(NumImange == 1):
                    break
                else:
                    # Añadimos 1 al contador de imagenes
                    NumImange = NumImange + 1
                    #print(datetime.strptime(str(post.date_utc), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y"))
                    print(ghost.username, "\t\t", datetime.strptime(str(post.date_utc), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y"))