import pyodbc
from io import StringIO
import csv
from datetime import datetime
server = 'medical-record-db.privatelink.database.windows.net'
database = 'med-record-sql'
username = 'sql_user'
password = '{Password12345*}'   
driver= '{ODBC Driver 17 for SQL Server}'
#conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
#cursor=conn.cursor()

def createUserTable():
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		cursor.execute("CREATE TABLE [User](username VARCHAR(50) UNIQUE, email VARCHAR(50), name VARCHAR(50), fln VARCHAR(50))")
		cursor.commit()
		conn.close()
	except:
		pass

def addUser(username, email, name, fln):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command = 'INSERT INTO [User] VALUES (?,?,?,?)'	
		cursor.execute(command,username,email,name,fln)
		cursor.commit()
		conn.close()
	except:
		createUserTable()
		try:
			conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
			cursor=conn.cursor()
			command = 'INSERT INTO [User] VALUES (?,?,?)'	
			cursor.execute(command,username,email,name)
			cursor.commit()
			conn.close()
		except:
			pass

def getFileFromUsername(username):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT fln FROM [User] WHERE username=?'
		cursor.execute(command,username)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue		 
	except:
		return "00"		
	
def getEmailFromUsername(username):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT email FROM [User] WHERE username=?'
		cursor.execute(command,username)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue		 
	except:
		return "00"
		
def getNameFromUsername(username):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT name FROM [User] WHERE username=?'
		cursor.execute(command,username)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue
		 
	except:
		return "00"

def getUserCount():
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT COUNT(*) FROM [User]'
		cursor.execute(command)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue
	except:
		return "00"
	
def createTagsTable():
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		cursor.execute("CREATE TABLE [Tags](username VARCHAR(50), tagid VARCHAR(50) UNIQUE, name VARCHAR(50), expiry VARCHAR(50))")
		cursor.commit()
		conn.close()
	except:
		pass

def addTag(username, tagid, name, expiry):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command = 'INSERT INTO [Tags] VALUES (?,?,?,?)'	
		cursor.execute(command,username,tagid,name,expiry)
		cursor.commit()
		conn.close()
	except:
		createTagsTable()
		try:
			conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
			cursor=conn.cursor()
			command = 'INSERT INTO [Tags] VALUES (?,?,?,?)'	
			cursor.execute(command,username,tagid,name,expiry)
			cursor.commit()
			conn.close()
		except:
			pass

def getUsernameFromTag(tagid):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT username FROM [Tags] WHERE tagid=?'
		cursor.execute(command,tagid)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue
	except:
		return "00"

def getExpiryFromTag(tagid):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT expiry FROM [Tags] WHERE tagid=?'
		cursor.execute(command,tagid)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue
	except:
		return "00"
		
def getNameFromTag(tagid):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT name FROM [Tags] WHERE tagid=?'
		cursor.execute(command,tagid)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue
	except:
		return "00"

def deleteTag(tagid):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command='DELETE FROM [Tags] WHERE tagid=?'
		cursor.execute(command,tagid)
		cursor.commit()
		conn.close()
	except:
		pass
		
def createFileTable():
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		cursor.execute("CREATE TABLE [File](username VARCHAR(50), test VARCHAR(50), dt VARCHAR(50), uploader VARCHAR(50), filename VARCHAR(50) UNIQUE)")
		cursor.commit()
		conn.close()
	except:
		pass

def addFile(username, test, dt, uploader, filename):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command = 'INSERT INTO [File] VALUES (?,?,?,?,?)'	
		cursor.execute(command,username, test, dt, uploader, filename)
		cursor.commit()
		conn.close()
	except:
		createFileTable()
		try:
			conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
			cursor=conn.cursor()
			command = 'INSERT INTO [File] VALUES (?,?,?,?,?)'	
			cursor.execute(command,username, test, dt, uploader, filename)
			cursor.commit()
			conn.close()
		except:
			pass
			
def getUserFromFile(filename):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT username FROM [File] WHERE filename=?'
		cursor.execute(command,filename)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue
	except:
		return "00"
	
def getTestFromFile(filename):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT test FROM [File] WHERE filename=?'
		cursor.execute(command,filename)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue
	except:
		return "00"

def getDateFromFile(filename):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT dt FROM [File] WHERE filename=?'
		cursor.execute(command,filename)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue
	except:
		return "00"

def getUploaderFromFile(filename):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT uploader FROM [File] WHERE filename=?'
		cursor.execute(command,filename)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue
	except:
		return "00"
	
def getFileListFromUser(user):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
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
		conn.close()
		return op
	except:
		return "Error"
		
def createDigestTable():
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		cursor.execute("CREATE TABLE [Msgdigest](filename VARCHAR(50), dgst VARCHAR(100))")
		cursor.commit()
		conn.close()
	except:
		pass

def addDigest(filename, dgst):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command = 'INSERT INTO [Msgdigest] VALUES (?,?)'	
		cursor.execute(command,filename,dgst)
		cursor.commit()
		conn.close()
	except:
		createDigestTable()
		try:
			conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
			cursor=conn.cursor()
			command = 'INSERT INTO [Msgdigest] VALUES (?,?)'	
			cursor.execute(command,filename,dgst)
			cursor.commit()
			conn.close()
		except:
			pass
	
def getDigestFromFile(filename):
	try:
		
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT dgst FROM [Msgdigest] WHERE filename=?'
		cursor.execute(command,filename)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue
	except:
		return "00"
	
def createAuditTable():
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		cursor.execute("CREATE TABLE [Adlog](tstp VARCHAR(50), username VARCHAR(50), test VARCHAR(50), dt VARCHAR(50), nm VARCHAR(50), addr VARCHAR(20), filename VARCHAR(50), mode VARCHAR(50), oper VARCHAR(50))")
		cursor.commit()
		conn.close()
	except:
		pass
	
def addAuditRecord(username, test, dt, nm, addr, filename,mode,oper):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command = 'INSERT INTO [Adlog] VALUES (?,?,?,?,?,?,?,?,?)'
		tstp=str(datetime.now())
		cursor.execute(command,tstp,username,test,dt,nm,addr,filename,mode,oper)
		cursor.commit()
		conn.close()
	except:
		createAuditTable()
		try:
			conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
			cursor=conn.cursor()
			command = 'INSERT INTO [Adlog] VALUES (?,?,?,?,?,?,?,?,?)'
			tstp=str(datetime.now())
			cursor.execute(command,tstp,username,test,dt,nm,addr,filename,mode,oper)
			cursor.commit()
			conn.close()
		except:
			pass
	
def readAudit():
	conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor=conn.cursor()
	k="Timestamp, Username, Test name, Date, Operator, IP Address, Filename, Mode, Operation\n"
	command= 'SELECT * FROM [Adlog]'
	cursor.execute(command)
	retValue=cursor.fetchall()
	cursor.commit()
	conn.close()
	for i in retValue:
		for x in range (0,9):
			k=k+i[x]+", "
		k=k[:-2]
		k=k+"\n"
	return k
		
def createAuthTable():
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		cursor.execute("CREATE TABLE [Auth](username VARCHAR(50), token VARCHAR(50) UNIQUE)")
		cursor.commit()
		conn.close()
	except:
		pass

def addToken(username, token):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command = 'INSERT INTO [Auth] VALUES (?,?)'	
		cursor.execute(command,username,token)
		cursor.commit()
		conn.close()
	except:
		createAuthTable()
		try:
			conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
			cursor=conn.cursor()
			command = 'INSERT INTO [Auth] VALUES (?,?)'	
			cursor.execute(command,username,token)
			cursor.commit()
			conn.close()
		except:
			pass
			
def getUsernameFromToken(token):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command ='SELECT username FROM [Auth] WHERE token=?'
		cursor.execute(command,token)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		conn.close()
		return retValue
	except:
		return "00"


def deleteToken(token):
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command='DELETE FROM [Auth] WHERE token=?'
		cursor.execute(command,token)
		cursor.commit()
		conn.close()
	except:
		pass

def resetDb():
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command='DROP table [User];'
		cursor.execute(command)
		cursor.commit()
		conn.close()
	except:
		pass
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command='DROP table [Tags];'
		cursor.execute(command)
		cursor.commit()
		conn.close()
	except:
		pass
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command='DROP table [File];'
		cursor.execute(command)
		cursor.commit()
		conn.close()
	except:
		pass
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command='DROP table [Auth];'
		cursor.execute(command)
		cursor.commit()
		conn.close()
	except:
		pass
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command='DROP table [Adlog];'
		cursor.execute(command)
		cursor.commit()
		conn.close()
	except:
		pass
	try:
		conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor=conn.cursor()
		command='DROP table [Msgdigest];'
		cursor.execute(command)
		cursor.commit()
		conn.close()
	except:
		pass

def createAllTables():
	createUserTable()
	createTagsTable()
	createFileTable()
	createAuthTable()
	createAuditTable()
	createDigestTable()
