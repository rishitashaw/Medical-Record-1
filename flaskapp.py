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
import pickle
import string
import random
import os
import uuid

url="medrecord.eastus.cloudapp.azure.com"
filepth='/home/vm_user/medrecords/'

createAllTables()

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
	em2=getEmailFromUsername(uname)
	if not em2=="00":
		return render_template("error.html", reason="Username already exists");
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
		addUser(uname,eml,name)
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
	encuname=encr(uname)
	resp=make_response(redirect("/dashboard"))
	resp.set_cookie("id",encuname)
	resp.set_cookie("type","admin")
	return resp

@app.route("/tagreg", methods=["GET","POST"])
def tagreg():
	return render_template("tagreg.html")
	
@app.route("/inittag", methods=["GET", "POST"])
def inittag():
	uname=decr(request.cookies.get("id"))
	exp=request.form['exp'].strip()
	iname=request.form['iname'].strip()
	tagid=uuid.uuid4()
	addTag(uname,tagid,iname,exp)
	return render_template("webnfc.html", scanbuttonparam="hidden", writebuttonparam="", token=tagid)
	
@app.route("/fidoreg", methods=["GET","POST"])
def fidoreg():
	encuname=request.cookies.get("id")
	uname=decr(encuname)
	resp= make_response(render_template("register.html",encuname=encr(uname)))
	resp.set_cookie("username",uname,max_age=60*60*24*365*50)
	return resp
	
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
	type=request.cookies.get('type')
	if type=="admin":
		return render_template("dashboard_admin.html")
	if type=="user":
		return render_template("dashboard_user.html")
	return render_template("error.html", reason="Cookies error")

@app.route("/fileupload", methods=["GET", "POST"])
def fileupload():
	return render_template("fileupload.html")
	
@app.route("/uploaddone", methods=["GET", "POST"])
def uploaddone():
	type=request.cookies.get('type')
	uname="00"
	upl="00"
	if type=="admin":
		uname=decr(request.cookies.get("id"))
		upl=uname
	if type=="user":
		token=request.cookies.get("id")
		if not tokenValid(token):
			return render_template("error.html", reason="Token expired")
		uname=getUsernameFromTag(token)
		upl=getNameFromTag(token)
	fln=str(uuid.uuid4())
	fln=fln+'.pdf'
	if 'file' not in request.files:
		return render_template("error.html", reason="File error")
	tname=request.form['tname']
	tdate=request.form['tdate']
	file=request.files['file']
	file.save(filepth+"userfiles/"+fln)
	addFile(uname,tname,tdate,upl,fln)
	eml=getEmailFromUsername(uname)
	nm=getNameFromUsername(uname)
	try:
		sendEmailNotifAdd(eml,tname,tdate,upl,nm)
	except:
		pass
	return redirect("/dashboard")

@app.route("/filedownload", methods=["GET","POST"])
def filedownload():
	type=request.cookies.get('type')
	uname="00"
	if type=="admin":
		uname=decr(request.cookies.get("id"))
		print(uname, "admin")
	if type=="user":
		token=request.cookies.get("id")
		if not tokenValid(token):
			return render_template("error.html", reason="Token expired")
		uname=getUsernameFromTag(token)
	print(uname)
	tabdata=getFileListFromUser(uname)
	try:
		em=getEmailFromUsername(uname)
		name=getNameFromUsername(uname)
		sendEmailNotifAdd(em,tname,tdate,upl,name)
	except:
		pass
	return render_template("filedownload.html",table_data=tabdata)

@app.route("/downloadfile", methods=["GET","POST"])
def downloadfile():
	uname="00"
	type=request.cookies.get('type')
	if type=="admin":
		uname=decr(request.cookies.get("id"))
	if type=="user":
		token=request.cookies.get("id")
		if not tokenValid(token):
			return render_template("error.html", reason="Token expired")
		uname=getUsernameFromTag(token)
	fln=request.args.get('name')
	uname2=getUserFromFile(fln)
	if not uname==uname2:
		return render_template("error.html", reason="Unauthorized access")
	return send_file(filepth+"userfiles/"+fln, as_attachment=True)
	
@app.route("/inittagread", methods=["GET","POST"])
def inittagread():
	return render_template("webnfc.html", scanbuttonparam="", writebuttonparam="hidden", token="Null")
	
@app.route("/readtag", methods=["GET", "POST"])
def readtag():
	tag=request.args.get('tagid')
	token=tag[4:].strip()
	if not tokenValid(token):
		return render_template("error.html", reason="Token expired")
	resp=make_response(redirect("/dashboard"))
	resp.set_cookie("id",token)
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
		encuname=encr(uname)
		resp=make_response(redirect("/dashboard"))
		resp.set_cookie("id",encuname)
		resp.set_cookie("type","admin")
		return resp
	else:
		return render_template("error.html", reason="Incorrect OTP")

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

    
def encr(wrd):
	return f1.encrypt(wrd.encode()).decode()
	
def decr(tok):
	return f1.decrypt(tok.encode()).decode()

def save_key(uname, credentials):
	with open(filepth+'cryptofiles/'+uname+'datafilekey.pkl','wb') as outp1:
		pickle.dump(credentials,outp1,pickle.HIGHEST_PROTOCOL)
		
def read_key(uname):
	try:
		with open(filepth+'cryptofiles/'+uname+'datafilekey.pkl', 'rb') as inp:
			temp = pickle.load(inp)
			return temp
	except:
		print("no cred data")
		return []

if __name__ == "__main__":
	app.run(ssl_context="adhoc", host='0.0.0.0', port=8080, debug=False)
