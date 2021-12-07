import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date
from configparser import ConfigParser


# ------------------------------------------------------------------------------------------------------------------------
# Variales
# ------------------------------------------------------------------------------------------------------------------------
today = date.today()

# Fichero de configuracion.
config = ConfigParser()
config.read("config.ini")

# Argumentos
args = aux_funcs.get_args()


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
# Numero TOTAL IMAGENES subidas
# ##########################################################################################################################
def Post():
    ConnectShowTotalComments=ConnectBBDD.cursor()
    ConnectShowTotalComments.execute(
        "SELECT total_post FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    SqlShowTotalNumComments = (str(*ConnectShowTotalComments.fetchone()))
    print("Total imagenes: " + color.OKGREEN + SqlShowTotalNumComments + color.ENDC)



# ##########################################################################################################################
# Numero TOTAL LIKES
# ##########################################################################################################################
def Likes():
    ConnectShowTotalLikes=ConnectBBDD.cursor()
    ConnectShowTotalLikes.execute(
        "SELECT total_likes FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    SqlShowTotalNumLikes = (str(*ConnectShowTotalLikes.fetchone()))
    print("Total Likes: " + color.OKGREEN + SqlShowTotalNumLikes + color.ENDC)



# ##########################################################################################################################
# Numero TOTAL COMENTARIOS
# ##########################################################################################################################
def Comments():
    ConnectShowTotalComments=ConnectBBDD.cursor()
    ConnectShowTotalComments.execute(
        "SELECT total_comments FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    SqlShowTotalNumComments = (str(*ConnectShowTotalComments.fetchone()))
    print("Total Comentarios: " + color.OKGREEN + SqlShowTotalNumComments + color.ENDC)



# ##########################################################################################################################
# Numero TOTAL Followers
# ##########################################################################################################################
def Followers():
    ConnectShowTotalFollowers=ConnectBBDD.cursor()
    ConnectShowTotalFollowers.execute(
        "SELECT count_followers FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    SqlShowTotalNumFollowers = (str(*ConnectShowTotalFollowers.fetchone()))
    print("Total Followers: " + color.OKGREEN + SqlShowTotalNumFollowers + color.ENDC)



# ##########################################################################################################################
# Numero TOTAL Followees
# ##########################################################################################################################
def Followees():
    ConnectShowTotalFollowees=ConnectBBDD.cursor()
    ConnectShowTotalFollowees.execute(
        "SELECT count_followees FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    SqlShowTotalNumFollowees = (str(*ConnectShowTotalFollowees.fetchone()))
    print("Total Followees: " + color.OKGREEN + SqlShowTotalNumFollowees + color.ENDC)



# ##########################################################################################################################
# Mostrar el engadment actuales desde la base de datos
# ##########################################################################################################################
def Engagement():
    ConnectShowEngagement=ConnectBBDD.cursor()
    ConnectShowEngagement.execute(
        "SELECT engagement FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    SqlShowEngagement = (str(*ConnectShowEngagement.fetchone()))
    print("Engagement: " + color.OKGREEN + SqlShowEngagement + color.ENDC)
