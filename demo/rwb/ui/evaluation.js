
// Transform coordinates -env["height"]-5 || env["width"]-5
function trC(coord, hw) {
	if (hw == 0) {
		return -(env["height"] * 10 / 2) + 5 + coord * 10;
	} else {
		return -(env["width"] * 10 / 2) + 5 + coord * 10;
	}

}
function colourSurroundings(x,y){
	resetColours();
	for(var i=(x-env["visibleRad"]);i<(x+1+env["visibleRad"]);i++){
		for(var j=(y-env["visibleRad"]);j<(y+1+env["visibleRad"]);j++){
			if ((-1<i)&&(i<env["height"])&&(-1<j)&&(j<env["width"])){
				if (env["paddingStates"].indexOf(JSON.stringify([i,j]))!= -1){
					scene.getObjectByName("cells").getObjectByName("padding").getObjectByName(i.toString()+'-'+j.toString()).material.color = new THREE.Color(0xff0000);
				}else{
					scene.getObjectByName("cells").getObjectByName("surface").getObjectByName(i.toString()+'-'+j.toString()).material.color = new THREE.Color(0xff0000);
				}
			}
		}
	}
}

function checkAgentOrientation(state, prevstate){
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
		new_orientation = agent_orientation;
	}
	if (new_orientation!=-1){
		var steps = (agent_orientation-new_orientation);

		if (steps>2){
			steps=-1;
		}else if (steps<-2){
			steps=1;
		}
		rotateAgent(0,steps*Math.PI/2,0,parseInt(velocity/2));
		agent_orientation = new_orientation;
	}


}

function runEvaluations(csvData, epoch) {
	// console.log("run evaluation");

	if (counter >= csvData.length - 1) {
		iterations();
	}else{
		state = [parseInt(csvData[counter][0]), parseInt(csvData[counter][1])];
		if (counter == 0 ){
			if (scene.getObjectByName("life")){
				removeHealthIndicators();
			}
			createLife();
			laststep=state;
			scene.getObjectByName("agent").rotation.y = 0;
			agent_orientation=1;
			hist = [];
		}else{
			reduceLife(csvData[counter][2]);
		}
		if ((env["wallStates"].indexOf(JSON.stringify(state)) != -1) && JSON.stringify(hist).indexOf(JSON.stringify(state)) == -1){
			flushReward((state[1] + state[0] * (width-1)).toString());
		}
		hist.push(state);
		checkAgentOrientation(state,laststep);
		if(laststep[0]==state[0] && laststep[1]==state[1] && counter != 0){
			if (state[0]==(env["height"]-1)){
				moveAgent(trC(state[0]+1,0), 5.5,trC(state[1],1), parseInt(velocity/2),0);
				moveAgent(trC(state[0],0), 5.5,trC(state[1],1), parseInt(velocity/2), parseInt(velocity/2));
			}else if(state[1]==(env["width"]-1)){
				moveAgent(trC(state[0],0), 5.5,trC(state[1]+1,1), parseInt(velocity/2), 0);
				moveAgent(trC(state[0],0), 5.5,trC(state[1],1), parseInt(velocity/2),parseInt(velocity/2));
			}else if(state[0]==0){
				moveAgent(trC(state[0]-1,0), 5.5,trC(state[1],1), parseInt(velocity/2),0);
				moveAgent(trC(state[0],0), 5.5,trC(state[1],1), parseInt(velocity/2),parseInt(velocity/2));
			}else if(state[1]==0){
				moveAgent(trC(state[0],0), 5.5,trC(state[1]-1,1), parseInt(velocity/2),0);
				moveAgent(trC(state[0],0), 5.5,trC(state[1],1), parseInt(velocity/2),parseInt(velocity/2));
			}
		}else{
			moveAgent(trC(state[0],0), 5.5,trC(state[1],1), velocity,0);
			colourSurroundings(state[0],state[1]);
		}
		if(scene.getObjectByName("health")){
			moveLife(trC(state[0],0), 5.5,trC(state[1],1), velocity,0);
		}
		laststep = state;
		counter += 1;
	}
}

function iterations() {
	if (epoch < env["epochs"]){
		counter = 0;
		if (scene.getObjectByName("cells")) {
			scene.remove(scene.getObjectByName("cells"));
		}
		loadEnvironment(algorithm, environment, epoch);
		showBoard();
		changeCSV(epoch.toString());
	}else{
		resetEnvironment();
	}
	epoch+=1;

}
