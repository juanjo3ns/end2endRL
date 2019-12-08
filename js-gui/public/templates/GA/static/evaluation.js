
// Transform coordinates -env["height"]-5 || env["width"]-5
function trC(coord, hw) {
	if (hw == 0) {
		return -(env["height"] * 10 / 2) + 5 + coord * 10;
	} else {
		return -(env["width"] * 10 / 2) + 5 + coord * 10;
	}
}

function checkAgentOrientation(state, prevstate, i){
	var new_orientation = -1;
	var state_dif = [state[0]-prevstate[0], state[1]-prevstate[1]];
	if (JSON.stringify(state_dif) == JSON.stringify([1,0])){
		new_orientation = 0;
	} else if (JSON.stringify(state_dif) == JSON.stringify([-1,0])){
		new_orientation = 2;
	} else if (JSON.stringify(state_dif) == JSON.stringify([0,-1])){
		new_orientation = 3;
	} else if(JSON.stringify(state_dif) == JSON.stringify([0,1])){
		new_orientation = 1;
	}else if(JSON.stringify(state_dif) == JSON.stringify([0,0])){
		new_orientation = orientations[i];
	}
	if (new_orientation!=-1){
		var steps = (orientations[i]-new_orientation);

		if (steps>2){
			steps=-1;
		}else if (steps<-2){
			steps=1;
		}
		rotateAgents(0, steps*Math.PI/2, 0, i, parseInt(velocity/2));
		orientations[i] = new_orientation;
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
		if (counter[i] == 0){
			laststep=state;
			scene.getObjectByName("agents").getObjectByName(i.toString()).rotation.y = 0;
			orientations[i]=1;
		}
		checkAgentOrientation(state,laststep,i);
		if(laststep[0]==state[0] && laststep[1]==state[1] && counter != 0){
			if (state[0]==(env["height"]-1)){
				moveAgents(trC(state[0]+1,0), 5.5,trC(state[1],1),i, parseInt(velocity/2),0);
				moveAgents(trC(state[0],0), 5.5,trC(state[1],1),i, parseInt(velocity/2), parseInt(velocity/2));
			}else if(state[1]==(env["width"]-1)){
				moveAgents(trC(state[0],0), 5.5,trC(state[1]+1,1),i, parseInt(velocity/2), 0);
				moveAgents(trC(state[0],0), 5.5,trC(state[1],1),i, parseInt(velocity/2),parseInt(velocity/2));
			}else if(state[0]==0){
				moveAgents(trC(state[0]-1,0), 5.5,trC(state[1],1),i, parseInt(velocity/2),0);
				moveAgents(trC(state[0],0), 5.5,trC(state[1],1),i, parseInt(velocity/2),parseInt(velocity/2));
			}else if(state[1]==0){
				moveAgents(trC(state[0],0), 5.5,trC(state[1]-1,1),i, parseInt(velocity/2),0);
				moveAgents(trC(state[0],0), 5.5,trC(state[1],1),i, parseInt(velocity/2),parseInt(velocity/2));
			}
		}else{
			moveAgents(trC(state[0],0), 5.5,trC(state[1],1),i, velocity,0);
		}
		if(scene.getObjectByName("health")){
			moveLife(trC(state[0],0), 5.5,trC(state[1],1),i, velocity,0);
		}
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
