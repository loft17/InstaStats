#!/usr/bin/env python3
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog

import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date
from configparser import ConfigParser

#from scripts import , , , 
#from scripts import , , resumeninfoaccount
#from scripts import , , , , ghostlastimg
#from scripts import , seguidoresperdidos, , test

from scripts import version, menuayuda
from scripts import reportgenerate, detailslastpost, showtotalnum, medianum, resumeninfoaccount
from scripts import showfollowers, showfollowees
from scripts import nofollowback, ghostlastimg, lostfollowers


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
# Comprobamos que no exite un reporte anterior para no volver a generarlo
# ##########################################################################################################################
def ReportStatus():
    ConnectReportStatus=ConnectBBDD.cursor()
    ConnectReportStatus.execute(
        "SELECT account FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
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
    ReportStatus()
    option = args.option

    if(option == "ayuda"):
        menuayuda.PrintUsage()

    elif(option == "help"):
        menuayuda.PrintUsage()    

    elif(option == "version"):
        version.VersionApp()

#..........................................................................
    elif(option == "detailslastpost"):
        detailslastpost.DetailsLastPost()



#..........................................................................
    elif(option == "numtotalpost"):
        showtotalnum.Post()

    elif(option == "numtotallikes"):
        showtotalnum.Likes()

    elif(option == "numtotalcomments"):
        showtotalnum.Comments()

    elif(option == "numtotalfollowers"):
        showtotalnum.Followers()

    elif(option == "numtotalfollowees"):
        showtotalnum.Followees()

    elif(option == "engagement"):     
        showtotalnum.Engagement()


#..........................................................................
    elif(option == "medialikes"):
        medianum.Likes()

    elif(option == "mediacomentarios"):
        medianum.Comments()


#..........................................................................
    elif(option == "followers"):
        showfollowers.ShowFollowers()

    elif(option == "followees"):
        showfollowees.ShowFollowees()


#..........................................................................
    elif(option == "nofollowback"):
        nofollowback.NoFollowBack()


#..........................................................................
    elif(option == "ghostlastimgfollowers"):
        ghostlastimg.LastFollowers()

    elif(option == "ghostlastimgfollowees"):
        ghostlastimg.LastFollowees()

    elif(option == "ghosttotalimgfollowees"):
        #ghostlastimg.TotalFollowees()
        print("Caracteristicas no disponible")

    elif(option == "ghosttotalimgfollowers"):
        #ghostlastimg.TotalFollowers()
        print("Caracteristicas no disponible")
    
    elif(option == "ghostlastimgfolloweesext"):
        ghostlastimg.LastFolloweesExt()



#..........................................................................
    elif(option == "seguidoresperdidos"):
        lostfollowers.SeguidoresPerdidos()


#..........................................................................
    elif(option == "resumeninfo"):
        resumeninfoaccount.ResumenInfoAccount()


#..........................................................................

    elif(option == "test"):
        #nofollowback.NoFollowBackExt()
        ghostlastimg.LastFollowees2()



#..........................................................................
    else:
        menuayuda.PrintUsage()

    # Cerramos la base de datos antes de que se cierre la aplicacion
    ConnectBBDD.close()
    print("")

if __name__ == "__main__":
		main()
