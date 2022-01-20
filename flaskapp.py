from __future__ import print_function, absolute_import, unicode_literals

from fido2.webauthn import PublicKeyCredentialRpEntity
from fido2.client import ClientData
from fido2.server import Fido2Server
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2 import cbor
from flask import *
from cryptography.fernet import Fernet
from datetime import datetime
from os import path
from sqloperations import *
from emailoperations import *
from storageoperations import *
import hashlib
import pickle
import string
import random
import os
import uuid
import re

url="medical-record.centralindia.cloudapp.azure.com"
filepth='/home/vm_user/medrecords/'
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

createAllTables()
createContainers()

app = Flask(__name__, static_url_path="")

if not path.exists(filepth+'appfiles/'+'medrecseckey.pkl'):
	outp3=open(filepth+'appfiles/'+'medrecseckey.pkl','wb')
	pickle.dump(os.urandom(32),outp3,pickle.HIGHEST_PROTOCOL)
	outp3.close()

inp3=open(filepth+'appfiles/'+'medrecseckey.pkl', 'rb')
app.secret_key = pickle.load(inp3)
inp3.close()

rp = PublicKeyCredentialRpEntity(url, "Medical Records")
server = Fido2Server(rp)

if not path.exists(filepth+'appfiles/'+'fernetkey1.pkl'):
	with open(filepth+'appfiles/'+'fernetkey1.pkl','wb') as outp1:
		pickle.dump(Fernet.generate_key(),outp1,pickle.HIGHEST_PROTOCOL)
		
inp1=open(filepth+'appfiles/'+'fernetkey1.pkl', 'rb')
key1=pickle.load(inp1)
inp1.close()
f1=Fernet(key1)

# Single user support.
credentials = []


@app.route("/")
def index():
	type=request.cookies.get("type")
	if type=="admin" or type=="user":
		return redirect("/dashboard")
	k=getUserCount()
	return render_template("index.html",ucount=k)
    
    
@app.route("/signup")
def signup():
	return render_template("signup.html")
	
@app.route("/signupresp", methods=["GET","POST"])
def signupresp():
	name=request.form['name'].strip()
	uname=request.form['uname'].strip()
	eml=request.form['eml'].strip()
	if not uname.isalnum():
		return render_template("error.html", reason="Username should be alphanumeric")
	if not isValidEmail(eml):
		return render_template("error.html", reason="Invalid email")
	em2=getEmailFromUsername(uname)
	if not em2=="00":
		return render_template("error.html", reason="Username already exists")
	otp=genOtp()
	encname=encr(name)
	encuname=encr(uname)
	enceml=encr(eml)
	encotp=encr(otp)
	sendEmail(eml,otp)
	return render_template("otpinput.html",encotp=encotp,encname=encname,enceml=enceml,encuname=encuname)
	
@app.route("/otpinp", methods=["GET", "POST"])
def otpinp():
	otp=decr(request.form['encotp'])
	name=decr(request.form['encname'])
	uname=decr(request.form['encuname'])
	eml=decr(request.form['enceml'])
	inpotp=request.form['otp'].strip()
	if otp==inpotp:
		fln=str(uuid.uuid4())
		addUser(uname,eml,name,fln)
		print(uname,eml,name)
		resp= make_response(render_template("register.html",encuname=encr(uname)))
		resp.set_cookie("username",uname,max_age=60*60*24*365*50)
		return resp
	else:
		return render_template("error.html", reason="Incorrect OTP")

@app.route("/initlogin", methods=["GET", "POST"])
def initlogin():
	uname=request.cookies.get("username")
	if not uname:
		return render_template("username_setcookies.html")
	else:
		return redirect("/authenticate")

@app.route("/setcookie", methods=["GET", "POST"])
def setcookie():
	user=request.form['uname']
	resp= make_response(redirect("/authenticate"))
	resp.set_cookie("username",user,max_age=60*60*24*365*50)
	return resp

@app.route("/authenticate", methods=["GET", "POST"])
def authenticate():
	uname=request.cookies.get("username")
	token=uuid.uuid4()
	return render_template("authenticate.html", uname=uname, tok=token)

@app.route("/signin", methods=["GET", "POST"])
def signin():
	token=request.args.get('token')
	uname=getUsernameFromToken(token)
	deleteToken(token)
	uname=uname
	encuname=encr(uname+' '+request.remote_addr)
	resp=make_response(redirect("/dashboard"))
	resp.set_cookie("id",encuname, max_age=3600)
	resp.set_cookie("type","admin")
	return resp

@app.route("/tagreg", methods=["GET","POST"])
def tagreg():
	if checkValidCookie(request.cookies.get('id'),request.remote_addr):
		return render_template("tagreg.html")
	return redirect("/")
	
@app.route("/inittag", methods=["GET", "POST"])
def inittag():
	if checkValidCookie(request.cookies.get('id'),request.remote_addr):
		uname=getIdFromCookie(request.cookies.get("id"))
		exp=request.form['exp'].strip()
		iname=request.form['iname'].strip()
		tagid=uuid.uuid4()
		addTag(uname,tagid,iname,exp)
		return render_template("webnfc.html", scanbuttonparam="hidden", writebuttonparam="", token=tagid)
	return redirect("/")
	
@app.route("/fidoreg", methods=["GET","POST"])
def fidoreg():
	if checkValidCookie(request.cookies.get('id'),request.remote_addr):
		uname=getIdFromCookie(request.cookies.get("id"))
		resp= make_response(render_template("register.html",encuname=encr(uname)))
		resp.set_cookie("username",uname,max_age=60*60*24*365*50)
		return resp
	return redirect("/")

@app.route("/fidoregplatform", methods=["GET","POST"])
def fidoregplatform():
	if checkValidCookie(request.cookies.get('id'),request.remote_addr):
		uname=getIdFromCookie(request.cookies.get("id"))
		resp= make_response(render_template("register_platform.html",encuname=encr(uname)))
		resp.set_cookie("username",uname,max_age=60*60*24*365*50)
		return resp
	return redirect("/")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
	if checkValidCookie(request.cookies.get('id'),request.remote_addr):
		type=request.cookies.get('type')
		if type=="admin":
			uname=getIdFromCookie(request.cookies.get("id"))
			name=getNameFromUsername(uname)
			if name=="00":
				return redirect("/logout")
			return render_template("dashboard_admin.html", name=name)
		if type=="user":
			token=getIdFromCookie(request.cookies.get("id"))
			if not tokenValid(token):
				return render_template("error.html", reason="Token expired")
			uname=getUsernameFromTag(token)
			name=getNameFromUsername(uname)
			exp=getExpiryFromTag(token)
			hname=getNameFromTag(token)
			if name=="00":
				return redirect("/logout")
			return render_template("dashboard_user.html", name=name,expiry=exp,hname=hname)
	return redirect("/logout")

@app.route("/fileupload", methods=["GET", "POST"])
def fileupload():
	if checkValidCookie(request.cookies.get('id'),request.remote_addr):
		return render_template("fileupload.html")
	return redirect("/")	
	
@app.route("/uploaddone", methods=["GET", "POST"])
def uploaddone():
	if checkValidCookie(request.cookies.get('id'),request.remote_addr):
		type=request.cookies.get('type')
		uname="00"
		upl="00"
		if type=="admin":
			uname=getIdFromCookie(request.cookies.get("id"))
			upl=getNameFromUsername(uname)
		if type=="user":
			token=getIdFromCookie(request.cookies.get("id"))
			if not tokenValid(token):
				return render_template("error.html", reason="Token expired")
			uname=getUsernameFromTag(token)
			upl=getNameFromTag(token)
		if 'file' not in request.files:
			return render_template("error.html", reason="File error")
		tname=request.form['tname']
		tdate=request.form['tdate']
		file=request.files['file']
		uplflnext=path.splitext(file.filename)[1]
		if not (uplflnext=='.pdf' or uplflnext=='.xml'):
			return render_template("error.html", reason="Unsupported file")
		fln=str(uuid.uuid4())
		fln=fln+uplflnext
		if not uplDateValid(tdate):
			return render_template("error.html", reason="Invalid test date")
		uploadUserFileToBlob(file.read(),fln)
		addFile(uname,tname,tdate,upl,fln)
		dgst=getSHAStr(file.read())
		addDigest(fln,dgst)
		addAuditRecord(uname,tname,tdate,upl,fln,'Web','Upload')
		eml=getEmailFromUsername(uname)
		nm=getNameFromUsername(uname)
		try:
			sendEmailNotifAdd(eml,tname,tdate,upl,nm)
		except:
			pass
	return redirect("/dashboard")
	
@app.route("/api/reportupload", methods=["GET", "POST"])
def reportupload():
	tag=request.form['tag']
	token=tag[4:].strip()
	if not tokenValid(token):
		return "Token expired"
	tname=request.form['testname']
	tdate=request.form['testdate']
	if not uplDateValid(tdate):
		return "Invalid test date"
	uname=uname=getUsernameFromTag(token)
	upl=getNameFromTag(token)
	nm=getNameFromUsername(uname)
	eml=getEmailFromUsername(uname)
	file=request.files['file']
	uplflnext=path.splitext(file.filename)[1]
	if not (uplflnext=='.pdf' or uplflnext=='.xml'):
		return "Unsupported file"
	fln=str(uuid.uuid4())
	fln=fln+uplflnext
	uploadUserFileToBlob(file.read(),fln)
	dgst=getSHAStr(file.read())
	addDigest(fln,dgst)
	addFile(uname,tname,tdate,upl,fln)
	addAuditRecord(uname,tname,tdate,upl,fln,'API','Upload')
	try:
		sendEmailNotifAdd(eml,tname,tdate,upl,nm)
	except:
		pass
	return "File uploaded"
	
@app.route("/filedownload", methods=["GET","POST"])
def filedownload():
	if checkValidCookie(request.cookies.get('id'),request.remote_addr):
		type=request.cookies.get('type')
		uname="00"
		if type=="admin":
			uname=getIdFromCookie(request.cookies.get("id"))
			print(uname, "admin")
		if type=="user":
			token=getIdFromCookie(request.cookies.get("id"))
			if not tokenValid(token):
				return render_template("error.html", reason="Token expired")
			uname=getUsernameFromTag(token)
		print(uname)
		tabdata=getFileListFromUser(uname)
		return render_template("filedownload.html",table_data=tabdata)
	return redirect("/")

@app.route("/downloadfile", methods=["GET","POST"])
def downloadfile():
	if checkValidCookie(request.cookies.get('id'),request.remote_addr):
		uname="00"
		type=request.cookies.get('type')
		if type=="admin":
			uname=getIdFromCookie(request.cookies.get("id"))
		if type=="user":
			token=getIdFromCookie(request.cookies.get("id"))
			if not tokenValid(token):
				return render_template("error.html", reason="Token expired")
			uname=getUsernameFromTag(token)
		fln=request.args.get('name')
		uname2=getUserFromFile(fln)
		if not uname==uname2:
			return render_template("error.html", reason="Unauthorized access")
		file=getDownloadLink(fln)
		dgst1=getDigestFromFile(fln)
		dgst2=getSHAStr(file)
		if not dgst1==dgst2:
			return render_template("error.html", reason="File may have been tampered with.")
		tname=getTestFromFile(fln)
		tdate=getDateFromFile(fln)
		upl=getUploaderFromFile(fln)
		addAuditRecord(uname,tname,tdate,upl,fln,'Web','Download')
		output=make_response(file)
		downflnext=path.splitext(fln)[1]
		output.headers["Content-Disposition"] = "attachment; filename="+fln
		ext=downflnext[-3:]
		output.headers["Content-type"] = "application/"+ext
		return output
	return redirect("/")
	
@app.route("/inittagread", methods=["GET","POST"])
def inittagread():
	return render_template("webnfc.html", scanbuttonparam="", writebuttonparam="hidden", token="Null")
	
@app.route("/readtag", methods=["GET", "POST"])
def readtag():
	tag=request.args.get('tagid')
	token=tag[4:].strip()
	if not tokenValid(token):
		return render_template("error.html", reason="Token expired")
	tok=encr(token+' '+request.remote_addr)
	resp=make_response(redirect("/dashboard"))
	resp.set_cookie("id",tok, max_age=3600)
	resp.set_cookie("type","user")
	return resp

@app.route("/logout", methods=["GET","POST"])
def logout():
	resp=make_response(redirect("/"))
	resp.set_cookie("id",'',expires=0)
	resp.set_cookie("type",'',expires=0)
	return resp
	
@app.route("/clearcookies",methods=["GET","POST"])
def clearcookies():
	resp=make_response(redirect("/logout"))
	resp.set_cookie("username",'',expires=0)
	return resp
	
@app.route("/loginotp", methods=["GET","POST"])
def loginotp():
	uname=request.args.get('uname')
	eml=getEmailFromUsername(uname)
	if eml=="00":
		return render_template("error.html", reason="No such user")
	otp=genOtp()
	encuname=encr(uname)
	encotp=encr(otp)
	sendEmail(eml,otp)
	return render_template("loginotp.html",encotp=encotp,encuname=encuname)
	
@app.route("/loginotpinp", methods=["GET","POST"])
def loginotpinp():
	otp=decr(request.form['encotp'])
	uname=decr(request.form['encuname'])
	inpotp=request.form['otp'].strip()
	if otp==inpotp:
		encuname=encr(uname+' '+request.remote_addr)
		resp=make_response(redirect("/dashboard"))
		resp.set_cookie("id",encuname, max_age=3600)
		resp.set_cookie("type","admin")
		return resp
	else:
		return render_template("error.html", reason="Incorrect OTP")

@app.route("/api/register/beginplatform", methods=["GET","POST"])
def register_begin_platform():
    encuname=request.args.get('uname')
    uname=decr(encuname)
    credentials=read_key(uname)
    registration_data, state = server.register_begin(
        {
            "id": b"user_id",
            "name": uname,
            "displayName": uname,
            "icon": "https://example.com/image.png",
        },
        credentials,
        user_verification="discouraged",
        authenticator_attachment="platform",
    )

    session["state"] = state
    print("\n\n\n\n")
    print(registration_data)
    print("\n\n\n\n")
    return cbor.encode(registration_data)

	
@app.route("/api/register/begin", methods=["GET","POST"])
def register_begin():
    encuname=request.args.get('uname')
    uname=decr(encuname)
    credentials=read_key(uname)
    registration_data, state = server.register_begin(
        {
            "id": b"user_id",
            "name": uname,
            "displayName": uname,
            "icon": "https://example.com/image.png",
        },
        credentials,
        user_verification="discouraged",
        authenticator_attachment="cross-platform",
    )

    session["state"] = state
    print("\n\n\n\n")
    print(registration_data)
    print("\n\n\n\n")
    return cbor.encode(registration_data)

@app.route("/api/register/complete", methods=["GET","POST"])
def register_complete():
    encuname=request.args.get('uname')
    uname=decr(encuname)
    credentials=read_key(uname)
    data = cbor.decode(request.get_data())
    client_data = ClientData(data["clientDataJSON"])
    att_obj = AttestationObject(data["attestationObject"])
    print("clientData", client_data)
    print("AttestationObject:", att_obj)

    auth_data = server.register_complete(session["state"], client_data, att_obj)

    credentials.append(auth_data.credential_data)
    save_key(uname, credentials)
    print("REGISTERED CREDENTIAL:", auth_data.credential_data)
    return cbor.encode({"status": "OK"})


@app.route("/api/authenticate/begin", methods=["GET","POST"])
def authenticate_begin():
    uname=request.args.get('uname')
    credentials=read_key(uname)
    if not credentials:
        abort(404)

    auth_data, state = server.authenticate_begin(credentials)
    session["state"] = state
    return cbor.encode(auth_data)


@app.route("/api/authenticate/complete", methods=["GET","POST"])
def authenticate_complete():
    uname=request.args.get('uname')
    token=request.args.get('token')
    credentials=read_key(uname)
    if not credentials:
        abort(404)

    data = cbor.decode(request.get_data())
    credential_id = data["credentialId"]
    client_data = ClientData(data["clientDataJSON"])
    auth_data = AuthenticatorData(data["authenticatorData"])
    signature = data["signature"]
    print("clientData", client_data)
    print("AuthenticatorData", auth_data)

    server.authenticate_complete(
        session.pop("state"),
        credentials,
        credential_id,
        client_data,
        auth_data,
        signature,
    )
    print("ASSERTION OK")
    addToken(uname,token)
    return cbor.encode({"status": "OK"})
    
def tokenValid(token):
	now=datetime.now()
	dtm=now.strftime("%Y-%m-%d")
	tokendtm=getExpiryFromTag(token)
	if tokendtm=="00":
		return False
	currdt=datetime.strptime(dtm, "%Y-%m-%d")
	tokndt=datetime.strptime(tokendtm, "%Y-%m-%d")
	k=currdt<=tokndt
	if not k:
		deleteTag(token)
	return k

def uplDateValid(upldt):
	try:
		now=datetime.now()
		dtm=now.strftime("%Y-%m-%d")
		currdt=datetime.strptime(dtm, "%Y-%m-%d")
		upldt=datetime.strptime(upldt, "%Y-%m-%d")
		k=currdt>=upldt
		return k
	except:
		return False

def checkValidCookie(id, ip):
	try:
		token=decr(id)
		arr=token.split()
		return arr[1]==ip
	except:
		return False
	
def getIdFromCookie(id):
	token=decr(id)
	arr=token.split()
	return arr[0]

def isValidEmail(email):
	return re.match(regex,email)
    
def getSHA(data):
	sha256_hash = hashlib.sha256()
        sha256_hash.update(data.read())
	return sha256_hash.hexdigest()
	
def getSHAStr(data):
	sha256_hash = hashlib.sha256()
        sha256_hash.update(data)
	return sha256_hash.hexdigest()
	
def encr(wrd):
	return f1.encrypt(wrd.encode()).decode()
	
def decr(tok):
	return f1.decrypt(tok.encode()).decode()

def save_key(uname, credentials):
	fln=getFileFromUsername(uname)
	uploadCryptoFile(pickle.dumps(credentials),fln)
		
def read_key(uname):
	try:
		fln=getFileFromUsername(uname)
		return pickle.loads(downloadCryptoFile(fln))
	except:
		print("no cred data")
		return []

if __name__ == "__main__":
	app.run(ssl_context="adhoc", host='0.0.0.0', port=8080, debug=False)
