from django.shortcuts import render
import datetime, requests, json, logging,base64, re, os, time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Template, Context

def checkIfTokCurrent():
	print "check if tok current reached!"
	DIR_NAME = os.path.dirname(__file__)
	f = open(DIR_NAME+ "/tok", "r+b")
	s = f.readline()
	print "tok is " + s
	f.close()
	patEp = r'\d{10}'
	patmatch = re.search(patEp, s)
	print "is this right for ep?" + str(patmatch.group())
	currentEp = time.time()
	currentEp = int(currentEp)
	if ((currentEp - int(patmatch.group())) > 3400):
		return False
	else:
		return True

def readTok():
	r = {}
	DIR_NAME = os.path.dirname(__file__)
	f = open(DIR_NAME + "/tok", "r+b")
	s = f.readline()
	f.close()
	patTo = r'\w+'
	patmatch = re.match(patTo,s)
	tok = patmatch.group()
	r["access_token"] = tok
	return r

def writeTok(token):
	DIR_NAME = os.path.dirname(__file__)
	Ep = time.time()
	Ep = int(Ep)
	f = open(DIR_NAME + "/tok", "w")
	f.write(token + " " + str(Ep))
	f.close()	

def getOAuth():
	if(checkIfTokCurrent()):
		print "token is current!"
		r = readTok()
		return r
	else:
		print "token is not current! We'll get a new one!"
		DIR_NAME = os.path.dirname(__file__)
        	f = open(DIR_NAME+ "/username", "r+b")
		username = f.readline()
		f.close()
        	f = open(DIR_NAME+ "/password", "r+b")
		password = f.readline()
		f.close()
		url = "https://api.telstra.com/v1/oauth/token"
		params = {"client_id": username, "client_secret": password, "grant_type": "client_credentials", "scope":"WIFI"}
		r = requests.post(url, data=params)
		writeTok(r.json()['access_token'])
		return r.json()

def getWifiLocations(LATITUDE,LONGITUDE, TOKEN):
	print "get wifi locations reached!"
	print LATITUDE, LONGITUDE
	RADIUS="2000"
	url = "https://api.telstra.com/v1/wifi/hotspots?lat=" + LATITUDE + "&long=" + LONGITUDE + "&radius=" +RADIUS
	headers = {"Authorization": "Bearer " + TOKEN}
	print str(headers)
	print url
	try:
		r = requests.get(url, headers=headers)
	except:
		print "didn't work!" 
		print r.text
	try:
		return r.json()
	except:
		print "response wasn't json!"

def getLocation(request):
	print "getLocation reached!"
	data = {}
	params = {}
	lon = request.POST.get("lon", False)
	lat = request.POST.get("lat", False)
	DIR_NAME = os.path.dirname(__file__)
        f = open(DIR_NAME+ "/API_KEY", "r+b")
	API_KEY = f.readline()
	f.close()
	logger = logging.getLogger(__name__)
	i = 0

	if (lat and lon):
		print lat, lon
		lat = float(lat)
		lon = float(lon)
		try:
			lat = ("{0:.6f}".format(lat))
			lon = ("{0:.6f}".format(lon))
			lon = str(lon)
			lat = str(lat)
			print lat
			print lon
			data  = {"API_KEY": API_KEY}
		except:
			print "lon lat conversion borked or params borked!"
			data['Error'] = "Location info was unavailable! e1"
			return HttpResponse(data['Error'], content_type="application/json")
		try:
			tok = getOAuth()['access_token']
			print "token is" + tok
			resp = getWifiLocations(lat, lon, tok)
		except:
			data['Error'] = "Service unavailable, please try again later e2"
			return HttpResponse(data['Error'], content_type="application/json")
		try:
			i = json.dumps(resp).count("lat")
			zoomCount = countZoom(i)
			data['zoomCount'] = zoomCount
			print "count for lat objs in resp is " + str(i)
			print "resp is " + str(resp)
			for y in resp:
				params["address" + str(i)] = y["lat"], y["long"], y["address"]
				i = i-1
				print str(params)
				data['params'] = params
		except:
			data['Error'] = "Service unavailable, please try again later e3"
			return HttpResponse(data['Error'], content_type="application/json")
		data['latCenter'] = lat
		data['lonCenter'] = lon
		data['Error'] = "request worked OK"
	else:
		#data['Error'] = "Sorry couldn't read your address correctly!"
		return HttpResponseRedirect("/")
	return render_to_response("mapLocation.html", data)

def getHome(request):
	return render_to_response("Hello2.html")

def countZoom(results):
	if (results > 0  and results < 4):
		return 12
	elif (results > 4 and results < 6):
		return 13
	elif (results == 0):
		return 0
	elif (results > 6):
		return 14
