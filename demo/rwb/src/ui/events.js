
function onDocumentMouseDown(event) {
  event.preventDefault();
  mouse.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1;
  mouse.y = -(event.clientY / renderer.domElement.clientHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  var intersects1 = raycaster.intersectObjects(scene.children);
  var intersects2 = raycaster.intersectObjects(scene.getObjectByName('text_parent').children);
  if (intersects2.length > 0) {
    intersects = raycaster.intersectObjects(scene.getObjectByName('text_parent').children);
    if (envs.indexOf(intersects[0].object.name) != -1) {

      if (scene.getObjectByName("cells")) {
        scene.remove(scene.getObjectByName("cells"));
      }
      resetColor(envs);
      if (intersects[0].object.name == environment) {
        env = {};
        env_set = false;
        environment = undefined;
      } else {
        intersects[0].object.material.color = new THREE.Color(0xff0000);
        environment = intersects[0].object.name;
        env_set = true;
        generateBoard(algorithm, intersects[0].object.name);
      }

    }
  } else if (intersects1.length > 0) {
    if (intersects1[0].object.name == 'switch') {
      // var current = scene.getObjectByName("text_parent").visible;
      // scene.getObjectByName("text_parent").visible = !current;
      if (env_set) {
        if (pushed == -1) {
          resetEnvironment();
        }
        else {
          scene.getObjectByName("switch").position.z -= 3;
          rotateObject(pushed * 2 * Math.PI / 3, 0, 0, "text_parent", 1000);
          pushed *= -1;
        }
      }
    }else if (intersects1[0].object.name == 'vbar'){
      cur_pos = scene.getObjectByName("cursor").position.x/100;

      if (mouse.x < cur_pos && cur_pos > -(2*VEL_JUMP)){
        moveCursor(-1);
        barvel -= VEL_JUMP;
        conversion(barvel);
      }else if (mouse.x > cur_pos && cur_pos < (2*VEL_JUMP)){
        moveCursor(1);
        barvel += VEL_JUMP;
        conversion(barvel);
      }
    }
  }
}
