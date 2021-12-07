#!/usr/bin/env python3
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog

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
color = printcolors.bcolors()

statusvar = "0"

# Fichero de configuracion.
config = ConfigParser()
config.read("config.ini")



# ##########################################################################################################################
# VERSION
# ##########################################################################################################################
def VersionApp():
    print("Version del programa:", color.OKGREEN + (config.get('VERSION_APP', 'VersionApp')), color.ENDC, "(" + (config.get('VERSION_APP', 'FechaApp')) + ")" )

