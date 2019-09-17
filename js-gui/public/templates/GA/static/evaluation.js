
// Transform coordinates -env["height"]-5 || env["width"]-5
function trC(coord, hw) {
	if (hw == 0) {
		return -(env["height"] * 10 / 2) + 5 + coord * 10;
	} else {
		return -(env["width"] * 10 / 2) + 5 + coord * 10;
	}
}

function runEvaluations(csvData, i, epoch) {
	if (counter[i] >= csvData.length - 2) {
		deads[i]=1;
		scene.getObjectByName("agents").getObjectByName(i.toString()).material.color = new THREE.Color(0xff0000);
		if (!deads.includes(0)){
			clearInterval(intervals[environment][i]);
			clearAgents();
			iterations();
		}else{
			clearInterval(intervals[environment][i]);
		}
	}else{
		state = [parseInt(csvData[counter[i]][0]), parseInt(csvData[counter[i]][1])];
		moveAgents(trC(state[0], 0), 5, trC(state[1], 1), i.toString(), velocity, 0);
		laststep = state;
		counter[i] += 1;
	}
}

function iterations() {
	deads.fill(0);
	counter.fill(0);
	epoch+=1;
	if (epoch < env["epochs"]){
		for (var i = 0; i < env["numAgents"]; i++) {
			csvfile = getURL(algorithm, "current", i.toString(), "coords", epoch.toString());
			csvData = getData(csvfile);
			intervals[environment][i] = setInterval(runEvaluations, velocity, csvData, i, epoch);
		}
	}else{
		resetEnvironment();
	}
}
