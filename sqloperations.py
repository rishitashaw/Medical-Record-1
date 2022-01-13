import pyodbc
from io import StringIO
import csv
server = 'med-record.database.windows.net'
database = 'med-record-sql'
username = 'sql_user'
password = '{Password12345*}'   
driver= '{ODBC Driver 17 for SQL Server}'
conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor=conn.cursor()

def createUserTable():
	try:
		cursor.execute("CREATE TABLE [User](username VARCHAR(100) UNIQUE, email VARCHAR(100), name VARCHAR(100))")
		cursor.commit()
	except:
		pass

def addUser(username, email, name):
	try:
		command = 'INSERT INTO [User] VALUES (?,?,?)'	
		cursor.execute(command,username,email,name)
		cursor.commit()
	except:
		createUserTable()
		try:
			command = 'INSERT INTO [User] VALUES (?,?,?)'	
			cursor.execute(command,username,email,name)
			cursor.commit()
		except:
			pass

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


def createTagsTable():
	try:
		cursor.execute("CREATE TABLE [Tags](username VARCHAR(100), tagid VARCHAR(100) UNIQUE, name VARCHAR(100), expiry VARCHAR(100))")
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
		cursor.execute("CREATE TABLE [File](username VARCHAR(100), test VARCHAR(100), dt VARCHAR(100), uploader VARCHAR(100), filename VARCHAR(100) UNIQUE)")
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
		

def createAuthTable():
	try:
		cursor.execute("CREATE TABLE [Auth](username VARCHAR(30), token VARCHAR(100) UNIQUE)")
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

def createAllTables():
	createUserTable()
	createTagsTable()
	createFileTable()
	createAuthTable()
