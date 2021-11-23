import sys, json, requests, os
import argparse
import random

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--user', required=True, action='store', help='Username')
	parser.add_argument('-l', '--login', required=True, action='store', help='Password')
	parser.add_argument('-o', '--option', required=True, action='store', help='Option')

	my_args = parser.parse_args()
	return my_args