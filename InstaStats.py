#!/usr/bin/env python3
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog

import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date
from configparser import ConfigParser

from scripts import version, menuayuda, nofollowback, showfollowees, showfollowers, medianumcomments
from scripts import medianumlikes, totalnumfollowees, resumeninfoaccount, totalnumfollowers
from scripts import showengagementBBDD, totalnumpost, totalnumcomments, totalnumlikes, ghostlastimg
from scripts import detailslastpost, seguidoresperdidos, reportgenerate, test

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
        reportgenerate.ReportGenerate()
    #else:
    #    print("Ya existe un reporte generado anteriormente")













##########################################################################################################################
# Ejecucion
##########################################################################################################################
def main():
    #ReportStatus()
    option = args.option

    if(option == "ayuda"):
        menuayuda.PrintUsage()
    
    elif(option == "version"):
        version.VersionApp()

    elif(option == "numtotallikes"):
        totalnumlikes.TotalNumLikes()

    elif(option == "numtotalcomments"):
        totalnumcomments.TotalNumComments()

    elif(option == "numtotalpost"):
        totalnumpost.TotalNumPost()

    elif(option == "engagement"):
        showengagementBBDD.ShowEngagementBBDD()

    elif(option == "numtotalfollowers"):
        totalnumfollowers.TotalNumFollowers()

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

    elif(option == "ghostlastimgfollowers"):
        ghostlastimg.GhostLastImgFollowers()

    elif(option == "ghostlastimgfollowees"):
        ghostlastimg.GhostLastImgFollowees()

    elif(option == "ghosttotalimgfollowees"):
        ghostlastimg.GhostTotalImgFollowees()

    elif(option == "ghosttotalimgfollowers"):
        ghostlastimg.GhostTotalImgFollowers()

    elif(option == "detailslastpost"):
        detailslastpost.DetailsLastPost()

    elif(option == "resumeninfo"):
        resumeninfoaccount.ResumenInfoAccount()

    elif(option == "seguidoresperdidos"):
        seguidoresperdidos.SeguidoresPerdidos()

    elif(option == "test"):
        test.Test()

    elif(option == "help"):
        menuayuda.PrintUsage()

    else:
        menuayuda.PrintUsage()

    # Cerramos la base de datos antes de que se cierre la aplicacion
    ConnectBBDD.close()
    print("")

if __name__ == "__main__":
		main()
