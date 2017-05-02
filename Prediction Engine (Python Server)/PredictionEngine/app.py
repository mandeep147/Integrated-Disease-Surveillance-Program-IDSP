from flask import Flask, jsonify, request, redirect, url_for, render_template, Response
from flask_cors import CORS, cross_origin
#from bson import json_util
#import json
from PredictionEngine import predict

app = Flask(__name__)
CORS(app)

def getDb():
	from pymongo import MongoClient
	client = MongoClient("mongodb://idsp:idsp@ds023495.mlab.com:23495/idsp_db")
	db = client.idsp_db
	return db

def get_idspRecord(db, loc, diseases, date):
   #return db.traindata.find_one()
   #return db.traindata.find({"location" : int(loc)})
	documents = []
	cursor = db.traindata.find_one({"location" : int(loc), "disease" : int(diseases), "report-date" : date})
	#print cursor
	#print cursor["ycases"]
	if cursor is None:
		return None
	else:
		return cursor["ycases"]

def getDoctorById(db, id):
	document = db.docdata.find_one({"id": id},{'_id': False})
	if document is None:
		return None
	else:
		return document


@app.route("/")
def greet():
	return "It works!"


@app.route("/doctor", methods = ["GET"])
def getDoctorDetails():
	id = request.args.get('id')
	db = getDb()
	doc = getDoctorById(db, int(id))
	if doc is None:
		return "Doctor details not found for given id"
	else:
		return jsonify(doc)

@app.route("/predict", methods = ['GET'])
@cross_origin()
def getDetails():
	location = request.args.get('location')
	disease = request.args.get('disease')
	date = request.args.get('date')
	#print date
	db = getDb()
	ycases = get_idspRecord(db, location, disease, date)
	if ycases is None:
		return "No data found for combination of location, disease and date"
	else:
		result = predict.predictResult(int(location),int(disease),int(ycases))[0]
	#print result
	result1 = {'result' : result}
	return jsonify(result1)
			
@app.route("/reportcase", methods = [ 'GET' ])
def create_idspRecord():
	location = request.args.get('location')
	disease = request.args.get('disease')
	date = request.args.get('date')	
	ycases = request.args.get('cases')
	db = getDb()
	insertcase(db, location, disease, date, ycases)
	return "Inserted"
	

def insertcase(db, loc, diseases, date, cases):    
	cursor = db.traindata.find_one({"location" : int(loc), "disease" : int(diseases), "report-date" : date})
	if cursor is None:
		db.traindata.insert_one({ "report-date": date, "location":int(loc),"disease": int( diseases), "cases" : 0.0,"ycases":int(cases)})
		print '\Updated data successfully\n'
	else:
		ycases = int( cursor["ycases"])+int(cases)
		db.traindata.update(cursor, {'$set':{ "ycases": ycases}})    
		print '\Updated data successfully\n'	

@app.route("/predictLocation", methods = ['GET'])
def getLocation():
	disease = request.args.get('disease')
	date = request.args.get('date')
	ycases = []
	db = getDb()
	cursor = db.traindata.find({"report-date": date, "disease": int(disease)}, {'_id': False})
	if cursor is None:
		return "No data found"
	else:
		for document in cursor:
			ycases.append(document)
		#return jsonify(ycases)
		return jsonify(predict.predictResult(ycases["location"],ycases["disease"],ycases["ycases"] ))	
