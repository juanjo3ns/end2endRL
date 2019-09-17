function moveLife(x, y, z, time, delay) {
	new TWEEN.Tween(scene.getObjectByName("health").position)
		.to(scene.getObjectByName("health").position.clone().set(x, y, z), time)
		.delay(delay)
		.easing(TWEEN.Easing.Linear.None)
		.start();

}

function moveAgent(x, y, z, time, delay) {
	new TWEEN.Tween(scene.getObjectByName("agent").position)
		.to(scene.getObjectByName("agent").position.clone().set(x, y, z), time)
		.delay(delay)
		.easing(TWEEN.Easing.Linear.None)
		.start();

}
function moveAgents(x, y, z,agent, time, delay) {
	new TWEEN.Tween(scene.getObjectByName("agents").getObjectByName(agent.toString()).position)
		.to(scene.getObjectByName("agents").getObjectByName(agent.toString()).position.clone().set(x, y, z), time)
		.delay(delay)
		.easing(TWEEN.Easing.Linear.None)
		.start();

}

function moveWall(y, time, wall) {
	new TWEEN.Tween(scene.getObjectByName("cells").getObjectByName(wall).position)
		.to(scene.getObjectByName("cells").getObjectByName(wall).position.clone().setY(y), time)
		.easing(TWEEN.Easing.Quadratic.Out)
		.start();

}
function moveCamera(x, y, z, time) {
	new TWEEN.Tween(scene.getObjectByName("camera").position)
		.to(scene.getObjectByName("camera").position.clone().set(x, y, z), time)
		.easing(TWEEN.Easing.Quadratic.Out)
		.start();

}
function moveCursor(direction) {
	x_ = scene.getObjectByName("cursor").position.x + direction*VEL_JUMP;
	new TWEEN.Tween(scene.getObjectByName("cursor").position)
		.to({ x: x_ }, 200)
		.easing(TWEEN.Easing.Quadratic.Out)
		.start();

}
function rotateSteps(time) {
	new TWEEN.Tween(scene.getObjectByName("steps").position)
		.to(scene.getObjectByName("steps").position.clone().set(0, -85, 0), time)
		.delay(1000)
		.easing(TWEEN.Easing.Quadratic.Out)
		.start();

}
function rotateAgent(x, y, z, time) {
	y_ = (scene.getObjectByName("agent").rotation.y + y)
	// console.log("rotate",y_);
	new TWEEN.Tween(scene.getObjectByName("agent").rotation)
		.to({ y: y_ }, time)
		.easing(TWEEN.Easing.Quadratic.Out)
		.start();

}


function flushReward(wall){
	wall = 'l'+wall;
	// console.log(wall);
	new TWEEN.Tween(scene.getObjectByName("cells").getObjectByName(wall).position)
		.to(scene.getObjectByName("cells").getObjectByName(wall).position.clone().setY(500), 1000)
		.easing(TWEEN.Easing.Quintic.In)
		// .onComplete(function () {
		// 	scene.getObjectByName("cells").remove(scene.getObjectByName("cells").getObjectByName(wall));
		// })
		.start();
}
