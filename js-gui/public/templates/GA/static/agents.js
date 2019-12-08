function removeAgents(){
  for (var i=0;i<env["numAgents"];i++){
    scene.getObjectByName("agents").remove(scene.getObjectByName("agents").children[0]);
  }
}

function clearAgents(){
  var children_agents = scene.getObjectByName("agents").children;
  for (var i=0;i<children_agents.length;i++){
    children_agents[i].material.color = new THREE.Color(0xFFFFFF);
  }
}

function createAgents(callback) {

  var geometry = new THREE.SphereGeometry(5, 32, 32, 0, 6.3, 0, 3.4);
  var material = new THREE.MeshBasicMaterial({
    color: 0xFFDEB2
  });
  for (var i = 0; i < env["numAgents"]; i++) {
    var material = new THREE.MeshBasicMaterial({
      color: 0xFFFFFF
    });
    var sphere = new THREE.Mesh(geometry, material);
    sphere.name = i.toString();
    agents.add(sphere);
  }
  scene.add(agents);
  // for (var i = 0; i < env["numAgents"]; i++) {
  //   const j = i;
  //   const objLoader = new THREE.OBJLoader2();
  //   objLoader.loadMtl('/templates/models/bb8/bb-unit.mtl', null, (materials) => {
  //     objLoader.setMaterials(materials);
  //     objLoader.load('/templates/models/bb8/bb-unit.obj', (event) => {
  //       const root = event.detail.loaderRootNode;
  //       root.scale.set(2.4, 2.4, 2.4);
  //       root.name = j.toString();
  //       root.visible = true;
  //       root.position.set(45, -50, 200);
  //       root.rotation.y=0;
  //       agents.add(root);
  //     });
  //   });
  // }
  orientations = new Array(env["numAgents"]).fill(1);
  scene.add(agents);
  epoch = -1;
  deads = new Array(env["numAgents"]).fill(0);
  counter = new Array(env["numAgents"]).fill(0);
  callback();
}
