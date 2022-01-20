import pyodbc
from io import StringIO
import csv
from datetime import datetime
server = 'medical-record-db.privatelink.database.windows.net'
database = 'med-record-sql'
username = 'sql_user'
password = '{Password12345*}'   
driver= '{ODBC Driver 17 for SQL Server}'
conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor=conn.cursor()

def createUserTable():
	try:
		cursor.execute("CREATE TABLE [User](username VARCHAR(50) UNIQUE, email VARCHAR(50), name VARCHAR(50), fln VARCHAR(50))")
		cursor.commit()
	except:
		pass

def addUser(username, email, name, fln):
	try:
		command = 'INSERT INTO [User] VALUES (?,?,?,?)'	
		cursor.execute(command,username,email,name,fln)
		cursor.commit()
	except:
		createUserTable()
		try:
			command = 'INSERT INTO [User] VALUES (?,?,?)'	
			cursor.execute(command,username,email,name)
			cursor.commit()
		except:
			pass

def getFileFromUsername(username):
	try:
		command ='SELECT fln FROM [User] WHERE username=?'
		cursor.execute(command,username)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue		 
	except:
		return "00"		
	
def getEmailFromUsername(username):
	try:
		command ='SELECT email FROM [User] WHERE username=?'
		cursor.execute(command,username)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue		 
	except:
		return "00"
		
def getNameFromUsername(username):
	try:
		command ='SELECT name FROM [User] WHERE username=?'
		cursor.execute(command,username)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
		 
	except:
		return "00"

def getUserCount():
	try:
		command ='SELECT COUNT(*) FROM [User]'
		cursor.execute(command)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
		 
	except:
		return "00"


def createTagsTable():
	try:
		cursor.execute("CREATE TABLE [Tags](username VARCHAR(50), tagid VARCHAR(50) UNIQUE, name VARCHAR(50), expiry VARCHAR(50))")
		cursor.commit()
	except:
		pass

def addTag(username, tagid, name, expiry):
	try:
		command = 'INSERT INTO [Tags] VALUES (?,?,?,?)'	
		cursor.execute(command,username,tagid,name,expiry)
		cursor.commit()
	except:
		createTagsTable()
		try:
			command = 'INSERT INTO [Tags] VALUES (?,?,?,?)'	
			cursor.execute(command,username,tagid,name,expiry)
			cursor.commit()
		except:
			pass

def getUsernameFromTag(tagid):
	try:
		command ='SELECT username FROM [Tags] WHERE tagid=?'
		cursor.execute(command,tagid)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
	except:
		return "00"

def getExpiryFromTag(tagid):
	try:
		command ='SELECT expiry FROM [Tags] WHERE tagid=?'
		cursor.execute(command,tagid)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
	except:
		return "00"
		
def getNameFromTag(tagid):
	try:
		command ='SELECT name FROM [Tags] WHERE tagid=?'
		cursor.execute(command,tagid)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
	except:
		return "00"

def deleteTag(tagid):
	try:
		command='DELETE FROM [Tags] WHERE tagid=?'
		cursor.execute(command,tagid)
		cursor.commit()
	except:
		pass
		
def createFileTable():
	try:
		cursor.execute("CREATE TABLE [File](username VARCHAR(50), test VARCHAR(50), dt VARCHAR(50), uploader VARCHAR(50), filename VARCHAR(50) UNIQUE)")
		cursor.commit()
	except:
		pass

def addFile(username, test, dt, uploader, filename):
	try:
		command = 'INSERT INTO [File] VALUES (?,?,?,?,?)'	
		cursor.execute(command,username, test, dt, uploader, filename)
		cursor.commit()
	except:
		createFileTable()
		try:
			command = 'INSERT INTO [File] VALUES (?,?,?,?,?)'	
			cursor.execute(command,username, test, dt, uploader, filename)
			cursor.commit()
		except:
			pass
			
def getUserFromFile(filename):
	try:
		command ='SELECT username FROM [File] WHERE filename=?'
		cursor.execute(command,filename)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
	except:
		return "00"
	
def getTestFromFile(filename):
	try:
		command ='SELECT test FROM [File] WHERE filename=?'
		cursor.execute(command,filename)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
	except:
		return "00"

def getDateFromFile(filename):
	try:
		command ='SELECT dt FROM [File] WHERE filename=?'
		cursor.execute(command,filename)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
	except:
		return "00"

def getUploaderFromFile(filename):
	try:
		command ='SELECT uploader FROM [File] WHERE filename=?'
		cursor.execute(command,filename)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
	except:
		return "00"
	
def getFileListFromUser(user):
	try:
		op='\n'
		op=op+'<tr>\n'
		op=op+'<th>Test name</th>\n'
		op=op+'<th>Test date</th>\n'
		op=op+'<th>Uploader</th>\n'
		op=op+'<th>Link</th>\n'
		op=op+'</tr>\n'
		command= 'SELECT test, dt, uploader, filename FROM [File] where username=?'
		cursor.execute(command,user)
		retValue=cursor.fetchall()
		cursor.commit()
		print(retValue)
		for i in retValue:
			op=op+'<tr>\n'
			op=op+'<td>'+i[0]+'</td>\n'
			op=op+'<td>'+i[1]+'</td>\n'
			op=op+'<td>'+i[2]+'</td>\n'
			op=op+'<td><a class="btn" href="/downloadfile?name='+i[3]+'">Download</a></td>\n'
			op=op+"</tr>\n"
		op=op+"\n"
		if len(retValue) ==0:
			op='<tr><th> No report available. </th></tr>'
		return op
	except:
		return "Error"
		
def createAuditTable():
	try:
		cursor.execute("CREATE TABLE [Adlog](tstp VARCHAR(50), username VARCHAR(50), test VARCHAR(50), dt VARCHAR(50), nm VARCHAR(50), filename VARCHAR(50), mode VARCHAR(50), oper VARCHAR(50))")
		cursor.commit()
	except:
		pass
	
def addAuditRecord(username, test, dt, nm, filename,mode,oper):
	try:
		command = 'INSERT INTO [Adlog] VALUES (?,?,?,?,?,?,?)'
		tstp=str(datetime.now())
		cursor.execute(command,tstp,username,test,dt,nm,filename,mode,oper)
		cursor.commit()
	except:
		pass
	
def readAudit():
	k=""
	k=k+"Timestamp, Username, Test name, Date, Operator, Filename, Mode, Operation\n"
	command= 'SELECT * FROM [Adlog]'
	cursor.execute(command)
	retValue=cursor.fetchall()
	cursor.commit()
	for i in retValue:
		for x in range (0,8):
			k=k+i[x]+", "
		k=k+"\n"
	return k
		
def createAuthTable():
	try:
		cursor.execute("CREATE TABLE [Auth](username VARCHAR(50), token VARCHAR(50) UNIQUE)")
		cursor.commit()
	except:
		pass

def addToken(username, token):
	try:
		command = 'INSERT INTO [Auth] VALUES (?,?)'	
		cursor.execute(command,username,token)
		cursor.commit()
	except:
		createAuthTable()
		try:
			command = 'INSERT INTO [Auth] VALUES (?,?)'	
			cursor.execute(command,username,token)
			cursor.commit()
		except:
			pass
			
def getUsernameFromToken(token):
	try:
		command ='SELECT username FROM [Auth] WHERE token=?'
		cursor.execute(command,token)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
	except:
		return "00"


def deleteToken(token):
	try:
		command='DELETE FROM [Auth] WHERE token=?'
		cursor.execute(command,token)
		cursor.commit()
	except:
		pass

def resetDb():
	try:
		command='DROP table [User];'
		cursor.execute(command)
		cursor.commit()
	except:
		pass
	try:
		command='DROP table [Tags];'
		cursor.execute(command)
		cursor.commit()
	except:
		pass
	try:
		command='DROP table [File];'
		cursor.execute(command)
		cursor.commit()
	except:
		pass
	try:
		command='DROP table [Auth];'
		cursor.execute(command)
		cursor.commit()
	except:
		pass
	try:
		command='DROP table [Audit];'
		cursor.execute(command)
		cursor.commit()
	except:
		pass

def createAllTables():
	createUserTable()
	createTagsTable()
	createFileTable()
	createAuthTable()
	createAuditTable()
