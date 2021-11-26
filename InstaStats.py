#!/usr/bin/env python3
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog

import os, aux_funcs, argparse, re, menu_ayuda, printcolors
import instaloader
import mysql.connector

from datetime import date
from configparser import ConfigParser

from scripts import nofollowback, showfollowees, showfollowers, medianumcomments, medianumlikes, totalnumfollowees

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
# Mostramos la fecha del informe y la url de insta
# ##########################################################################################################################
def ShowInfgen():
    print("\nInforme generado el", color.OKCYAN, today, color.ENDC)
    print("url: https://www.instagram.com/" + PROFILE)
    print("")



# ##########################################################################################################################
# Mostramos un menu de ayuda para ejecutar correctamente la aplicacion
# ##########################################################################################################################
def MainMenu():
    menu_ayuda.PrintUsage()



# ##########################################################################################################################
# VERSION
# ##########################################################################################################################
def VersionApp():
    print("Version del programa:", color.OKGREEN + (config.get('VERSION_APP', 'VersionApp')), "(", (config.get('VERSION_APP', 'FechaApp')), ")" )



# ##########################################################################################################################
# Comprobamos que no exite un reporte anterior para no volver a generarlo
# ##########################################################################################################################
def ReportStatus():
    ConnectReportStatus=ConnectBBDD.cursor()
    ConnectReportStatus.execute(
        "SELECT account FROM ig_report WHERE date = %s AND account = %s", (today, PROFILE)
    )
    ConsultaSql = ConnectReportStatus.fetchone()  
    
    if(ConsultaSql == None):
        # No se ha generado anteriormente
        ReportGenerate()
    #else:
    #    print("Ya existe un reporte generado anteriormente")


# ##########################################################################################################################
# Generamos un reporte para guardar en la base de datos
# ##########################################################################################################################
def ReportGenerate():
    profile = instaloader.Profile.from_username(L.context, PROFILE)

    # ----------------------------------------------------------------------------------------------------------------------
    # Variables a 0
    # ----------------------------------------------------------------------------------------------------------------------    
    total_num_likes = 0
    total_num_comments = 0
    total_num_posts = 0
    total_num_followers = 0
    total_num_followees = 0
    listado_followees = []
    listado_followers = []



    # ----------------------------------------------------------------------------------------------------------------------
    # Conseguimos el Engagement, likes, coments, post actual y lo guardamos en la base de datos
    # ----------------------------------------------------------------------------------------------------------------------
    num_followers = profile.followers
    for post in profile.get_posts():
        total_num_likes += post.likes
        total_num_comments += post.comments
        total_num_posts += 1

    engagement = round((float(total_num_likes + total_num_comments) / (num_followers * total_num_posts) * 100), 2)
    #print(engagement)
    


    # ----------------------------------------------------------------------------------------------------------------------
    # Conseguimos los get_followees que nos siguien
    # ----------------------------------------------------------------------------------------------------------------------
    followees = profile.get_followees()
    for followee in followees:
        total_num_followees=total_num_followees+1
        listado_followees.append(followee.username)
        #print(followee.username)

    # ----------------------------------------------------------------------------------------------------------------------
    # Conseguimos los get_followers que nos siguien
    # ----------------------------------------------------------------------------------------------------------------------
    followers = profile.get_followers()
    for follower in followers:
        total_num_followers=total_num_followers+1
        listado_followers.append(follower.username)
        #print(follower.username)



    # ----------------------------------------------------------------------------------------------------------------------
    # Convertimos la lista en STR y eliminamos caracteres innecesarios para la base de datos
    # ----------------------------------------------------------------------------------------------------------------------
    characters = ",'[]"
    srt_followees = str(listado_followees)
    srt_followers = str(listado_followers)
    for x in range(len(characters)):
        srt_followees = srt_followees.replace(characters[x],"")
        srt_followers = srt_followers.replace(characters[x],"")



    # ----------------------------------------------------------------------------------------------------------------------
    # Sacamos el ID del usuario
    # ----------------------------------------------------------------------------------------------------------------------
    userid_account = re.sub('[^A-Za-z0-9]+', '', (str(profile).split("(", 1)[1]))



    # ----------------------------------------------------------------------------------------------------------------------
    # Guardamos toda la informacion en la base de datos
    # ----------------------------------------------------------------------------------------------------------------------
    ConnectInfo=ConnectBBDD.cursor()
    InsertInfo="insert into ig_report(date, account, userid, followers, followees, count_followers, count_followees, total_likes, total_comments, total_post, engagement) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    datos=(today, PROFILE, userid_account, srt_followers, srt_followees, total_num_followers, total_num_followees, total_num_likes, total_num_comments, total_num_posts, engagement)
    ConnectInfo.execute(InsertInfo, datos)
    
   
    # Guardamos la BBDD y la cerramos --------------------------------------------------------------------------------------
    ConnectBBDD.commit()



# ##########################################################################################################################
# Numero TOTAL LIKES
# ##########################################################################################################################
def TotalNumLikes():
    ConnectShowTotalLikes=ConnectBBDD.cursor()
    ConnectShowTotalLikes.execute(
        "SELECT total_likes FROM ig_report WHERE date = %s AND account = %s", (today, PROFILE)
    )
    SqlShowTotalNumLikes = (str(*ConnectShowTotalLikes.fetchone()))
    print("Total Likes: " + color.OKGREEN + SqlShowTotalNumLikes + color.ENDC)



# ##########################################################################################################################
# Numero TOTAL COMENTARIOS
# ##########################################################################################################################
def TotalNumComments():
    ConnectShowTotalComments=ConnectBBDD.cursor()
    ConnectShowTotalComments.execute(
        "SELECT total_comments FROM ig_report WHERE date = %s AND account = %s", (today, PROFILE)
    )
    SqlShowTotalNumComments = (str(*ConnectShowTotalComments.fetchone()))
    print("Total Comentarios: " + color.OKGREEN + SqlShowTotalNumComments + color.ENDC)



# ##########################################################################################################################
# Numero TOTAL IMAGENES subidas
# ##########################################################################################################################
def TotalNumPost():
    ConnectShowTotalComments=ConnectBBDD.cursor()
    ConnectShowTotalComments.execute(
        "SELECT total_post FROM ig_report WHERE date = %s AND account = %s", (today, PROFILE)
    )
    SqlShowTotalNumComments = (str(*ConnectShowTotalComments.fetchone()))
    print("Total imagenes: " + color.OKGREEN + SqlShowTotalNumComments + color.ENDC)



# ##########################################################################################################################
# Mostrar el engadment actuales desde la base de datos
# ##########################################################################################################################
def ShowEngagementBBDD():
    ConnectShowEngagement=ConnectBBDD.cursor()
    ConnectShowEngagement.execute(
        "SELECT engagement FROM ig_report WHERE date = %s AND account = %s", (today, PROFILE)
    )
    SqlShowEngagement = (str(*ConnectShowEngagement.fetchone()))
    print("Engagement: " + color.OKGREEN + SqlShowEngagement + color.ENDC)



# ##########################################################################################################################
# Numero TOTAL Followers
# ##########################################################################################################################
def TotalNumFollowers():
    ConnectShowTotalFollowers=ConnectBBDD.cursor()
    ConnectShowTotalFollowers.execute(
        "SELECT count_followers FROM ig_report WHERE date = %s AND account = %s", (today, PROFILE)
    )
    SqlShowTotalNumFollowers = (str(*ConnectShowTotalFollowers.fetchone()))
    print("Total Followers: " + color.OKGREEN + SqlShowTotalNumFollowers + color.ENDC)




















            









# ##########################################################################################################################
# Resumen Info cuenta
# ##########################################################################################################################
def ResumenInfoAccount():
    ShowInfgen()
    TotalNumFollowers()
    TotalNumFollowees()
    TotalNumLikes()
    TotalNumComments()
    TotalNumPost()
    ShowEngagementBBDD()
    MediaNumLikes()
    MediaNumComments()
    print("")



##########################################################################################################################
# Ejecucion
##########################################################################################################################
def main():
    ReportStatus()
    option = args.option

    if(option == "ayuda"):
        MainMenu()
    
    elif(option == "version"):
        VersionApp()

    elif(option == "numtotallikes"):
        TotalNumLikes()

    elif(option == "numtotalcomments"):
        TotalNumComments()

    elif(option == "numtotalpost"):
        TotalNumPost()

    elif(option == "engagement"):
        ShowEngagementBBDD()

    elif(option == "numtotalfollowers"):
        TotalNumFollowers()

    elif(option == "numtotalfollowees"):
        totalnumfollowees.TotalNumFollowees()

    elif(option == "medialikes"):
        medianumlikes.MediaNumLikes()

    elif(option == "mediacomentarios"):
        medianumcomments.MediaNumComments()

    elif(option == "followers"):
        showfollowers.ShowFollowers()

    elif(option == "followees"):
        showfollowees.ShowFollowees()

    elif(option == "nofollowback"):
        nofollowback.NoFollowBack()


    elif(option == "resumeninfo"):
        ResumenInfoAccount()





    elif(option == "help"):
        MainMenu()

    elif(option == "test"):
        totalnumfollowees.TotalNumFollowees()

    else:
        MainMenu()

    # Cerramos la base de datos antes de que se cierre la aplicacion
    ConnectBBDD.close()
    print("")

if __name__ == "__main__":
		main()
