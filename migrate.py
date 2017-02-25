#!/usr/bin/python3.4
import datetime
import pymongo
import os
import sys

from pymongo import MongoClient
from subprocess import call

def update(args):
	print('Beginning migrations...')

	HOST = 'localhost'
	PORT = 27017
	for index, arg in enumerate(args):
		if arg == '-h':
			HOST = args[index+1]
		if arg == '-p':
			PORT = int(args[index+1])

	client = MongoClient(HOST, PORT)
	dev_db = client.dev_db

	doc = dev_db.migrations.find_one(sort=[("timestamp", -1)])
	timestamp = int(doc['timestamp']) if doc is not None else 0
	files = get_files(timestamp)
	for file in files:
		print('Migrating: ' + file)
		#run the script...
		if call(['mongo','{0}:{1}'.format(HOST, PORT), '--eval','var conn=new Mongo(\'{0}:{1}\')'.format(HOST, PORT), file]) == 0:
			dev_db.migrations.insert({'timestamp':file_time(file), 'name': file})
		else:
			print('Migration: ' + file + ' failed. Stopping now!')
			sys.exit()
	print('All migrations have been ran')

new_file_setup = '//Created at: {0}\n' \
	'//Title: {1}\n' \
	'print("Running migration: {1}");\n\n' \
	'load("include.js");\n\n' \
	'//connection stored in variable "conn"' \
	'var db = conn.getDB("LifeTree");\n'

def create(args):
	print('Creating migration file...')
	timestamp = '{:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())
	filename = '{0}-{1}.js'.format("_".join(i.lower() for i in args), timestamp)
	print(filename)
	try:
		with open(filename, 'w+') as file:
			file.write(new_file_setup
				.format(timestamp, " ".join(args)))
		print('Migration file created: {0}'.format(filename))
	except Exception as e:
		print(e)
		print('Migrations file not created')

def file_time(filename):
	return filename.split('-')[-1][0:-3]

def get_files(timestamp):
	files = [i for i in os.listdir('.') if i not in [os.path.basename(__file__), "include.js", 'venv', 'README.md', 'LICENSE', 'requirements.txt']
		and int(file_time(i)) > timestamp]
	files.sort(key=file_time)
	return files

if __name__ == '__main__':
	commands = {
		'create': create,
		'update': update
	}
	command_names = (i.__name__ for i in commands)
	if len(sys.argv) >= 2 and sys.argv[1] in commands.keys():
		commands[sys.argv[1]](sys.argv[2:])
		sys.exit()
	print('Incorrect usage. You must provide 1 argument, either `create` or `update`')
