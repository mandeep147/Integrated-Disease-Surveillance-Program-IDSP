
const MONGODB_URL = "mongodb://localhost:27017/idsp";
//const MONGODB_URL = "mongodb://amazonfresh:amazonfresh@ds025180.mlab.com:25180/amazonfresh";
exports.MONGODB_URL = MONGODB_URL;
var MongoClient = require('mongodb').MongoClient;
var db;
var connected = false;
var pool = {
	_collections: {}
};
pool.getCollection = function (name) {
	if (!this._collections[name]) {
		this._collections[name] = db.collection(name);
	}
	return this._collections[name];
};


/**
 * Connects to the MongoDB Database with the provided URL
 */
exports.connect = function (url, callback) {
	MongoClient.connect(MONGODB_URL, {
		options: {
			server: {
				auto_reconnect: true,
				poolSize: 10,
				socketOptions: {
					keepAlive: 1
				}
			},
			db: {
				numberOfRetries: 10,
				retryMiliSeconds: 1000
			}
		}
	}, function (err, _db) {
		if (err) {
			throw new Error('Could not connect: ' + err);
		}
		db = _db;
		connected = true;
		callback(db);
	});
};

/**
 * Returns the collection on the selected database
 */
exports.collection = function (name) {
	return pool.getCollection(name);
};