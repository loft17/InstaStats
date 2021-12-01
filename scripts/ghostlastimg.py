#!/usr/bin/env python3
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog

import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date
from configparser import ConfigParser

from scripts import menuayuda, nofollowback, showfollowees, showfollowers, medianumcomments, medianumlikes, totalnumfollowees, resumeninfoaccount, totalnumfollowers, showengagementBBDD, totalnumpost, totalnumcomments, totalnumlikes, version, ghostlastimg



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
# GHOST LAST IMG FOLLOWERS
# ##########################################################################################################################
def GhostLastImgFollowers():
    profile = instaloader.Profile.from_username(L.context, PROFILE)
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
def GhostLastImgFollowees():
    profile = instaloader.Profile.from_username(L.context, PROFILE)
    NumImange = 0
    likes = set()

    #print("sacamos los likes")
    # Conseguimos todos los likes de las ultimas 10 imagenes
    for post in profile.get_posts():
        if(NumImange == 10):
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
def GhostTotalImgFollowers():
    profile = instaloader.Profile.from_username(L.context, PROFILE)
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
def GhostTotalImgFollowees():
    profile = instaloader.Profile.from_username(L.context, PROFILE)
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