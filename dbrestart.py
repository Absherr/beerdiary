import _mysql, _mysql_exceptions
import os

def connect():
    try:
        db=_mysql.connect(host="localhost",user="root", passwd="root")
	print "Connected!"
    	return db
    except _mysql_exceptions.OperationalError:
        print "Cannot connect to database!"
        return None

def drop(db, dbname):
    try:    
	db.query("DROP database "+dbname)
	print "Database has been dropped!"
	return True
    except _mysql_exceptions.OperationalError:
	print "Cannot drop database "+dbname+"!"
        return False

def create(db, dbname):
    try:    
	db.query("CREATE database "+dbname)
	print "Database has been created!"
	return True
    except _mysql_exceptions.OperationalError:
	print "Cannot create database "+dbname+"!"
        return False


def load_from_file(file_name):
    f = open(file_name)
    ans = []
    for line in f.readlines():
        line = line.strip()
        ans.append(line)
    return ans

dbname="beerdiarydb"

db = connect()
if db is not None:
    drop(db,dbname)
    create(db,dbname)
    os.system("python manage.py syncdb")
    
    db.query("use "+dbname)

    l = load_from_file('styles')
    for item in l:
	db.query("insert into beerdiary_beer_style (name) values ('"+item+"')")
    print "Beer styles inserted into db!"

    l = load_from_file('countries')
    for item in l:
	db.query("insert into beerdiary_country (name) values ('"+item+"')")
    print "Countries inserted into db!"

	
