import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date
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
def Likes():
    ConnectShowMediaLikes=ConnectBBDD.cursor()
    ConnectShowMediaLikes.execute(
        "SELECT total_likes FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    SqlShowMediaNumLikes = (int(*ConnectShowMediaLikes.fetchone()))
    
    ConnectShowMediaLikes.execute(
        "SELECT total_post FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    SqlShowMediaNumPost = (int(*ConnectShowMediaLikes.fetchone()))

    NumMediaLikesPosts = round(SqlShowMediaNumLikes / SqlShowMediaNumPost, 2)
    print("Media Likes por post: " + color.OKGREEN + str(NumMediaLikesPosts) + color.ENDC)



# ##########################################################################################################################
# Numero MEDIA COMENTARIOS por post
# ##########################################################################################################################
def Comments():
    ConnectShowMediaComments=ConnectBBDD.cursor()
    ConnectShowMediaComments.execute(
        "SELECT total_comments FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    SqlShowMediaNumComments = (int(*ConnectShowMediaComments.fetchone()))
    
    ConnectShowMediaComments.execute(
        "SELECT total_post FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    SqlShowMediaNumPost = (int(*ConnectShowMediaComments.fetchone()))

    NumMediaCommentsPosts = round(SqlShowMediaNumComments / SqlShowMediaNumPost, 2)
    print("Media comentarios por post: " + color.OKGREEN + str(NumMediaCommentsPosts) + color.ENDC)
