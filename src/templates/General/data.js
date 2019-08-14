function changeCSV(epoch) {
	clearInterval(intervalID);
	csvfile = getURL(algorithm, "current","0", "coords", epoch);
	csvData = getData(csvfile);
	intervalID = setInterval(runEvaluations, velocity, csvData, epoch);
}

function getURL(algorithm, environment, agent, type, epoch) {
	base = "/path/templates/csvdata/".concat(algorithm).concat('/').concat(environment).concat('/');
	return base.concat(agent).concat('/').concat(type).concat('/').concat(epoch).concat('.csv');
}

function getData(csv_file) {
	var url = csv_file;
	var request = new XMLHttpRequest();
	request.open("GET", url, false);
	request.send(null);

	var csvData = new Array();
	var jsonObject = request.responseText.split(/\r?\n|\r/);
	for (var t = 0; t < jsonObject.length; t++) {
		csvData.push(jsonObject[t].split(','));
	}
	return csvData;
}

function loadArray(array){
	var ar = new Array();
	for (var i = 0; i < array.length; i++) {
		if (i % 2 == 0) {
			var x = array[i];
		} else {
			ar.push(new Array(parseInt(x), parseInt(array[i])));
		}
	}
	return ar;
}
function loadValues(array){
	return new Array(array);
}

function loadEnvironment(algorithm, environment="current", counter) {
	csvfile = getURL(algorithm, environment,"0", "info", counter.toString());
	csvData = getData(csvfile);
	env["height"] = csvData[1][0];
	env["width"] = csvData[1][1];
	env["paddingStates"] = JSON.stringify(loadArray(csvData[2]));
	env["finalStates"] = JSON.stringify(loadArray(csvData[3]));
	env["wallStates"] = JSON.stringify(loadArray(csvData[4]));
	env["wallValues"] = csvData[5].map(parseFloat);
	env["numAgents"] = parseInt(csvData[6][0]);
	env["epochs"] = parseInt(csvData[7][0]);
	env["visibleRad"] = parseInt(csvData[8][0]);
	env["min_wall"] = parseInt(csvData[9][0]);
	env["max_wall"] = parseInt(csvData[9][1]);
}
