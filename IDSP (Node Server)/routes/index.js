var express = require('express');
var router = express.Router();
var MongoDB = require("./mongodbhandler");

/* GET home page. */
router.get('/', function (req, res, next) {
	res.render('index', {title: 'IDSP'});
});

router.get("/populateDB", function (req, res, next) {
	populateProducts();
	res.send("OK");
});

populateProducts = function () {
	var i = 0;

	function myLoop(i) {
		setTimeout(function () {
			console.log(i);
			if (i < 1673) {
				var oldVal = oldValues[i];
				var newVal = newValues[i];
				i++;
				var cursor = MongoDB.collection("traindata").update(
					{"data-field": oldVal},
					{
						$set: {
							"data-field": newVal
						}
					},
					{ multi: true }
				);
				cursor.then(function (error) {
					if(error) {
						console.log(error);
					}
					console.log("Replaced " + oldVal + " by " + newVal);
				}).catch(function (error) {
					console.log("Error replacing " + oldVal + " by " + newVal);
					console.log("Error: " + error);
				});
				myLoop(i);
			} else {
				return;
			}

		}, 50);
	}

	myLoop(i);
};

module.exports = router;
