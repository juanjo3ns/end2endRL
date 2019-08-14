function removeAgent(){
  scene.remove(scene.getObjectByName("agent"));
}

async function createAgent(callback) {

  const objLoader = new THREE.OBJLoader2();
  objLoader.loadMtl('../models/bb8/bb-unit.mtl', null, (materials) => {
    objLoader.setMaterials(materials);
    objLoader.load('../models/bb8/bb-unit.obj', (event) => {
      const root = event.detail.loaderRootNode;
      root.scale.set(2.4, 2.4, 2.4);
			root.name = 'agent';
      root.visible = false;
      root.position.set(45, -50, 200);
      root.rotation.y=0;
			scene.add(root);
    });
  });
}
