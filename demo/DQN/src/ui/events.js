function onDocumentMouseDown(event) {
  event.preventDefault();
  mouse.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1;
  mouse.y = -(event.clientY / renderer.domElement.clientHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  var intersects1 = raycaster.intersectObjects(scene.children);
  if (intersects1.length > 0) {
    if (intersects1[0].object.name == 'vbar'){
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
