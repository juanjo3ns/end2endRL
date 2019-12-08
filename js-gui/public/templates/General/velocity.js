//
// var velocity = 200;
// var barvel = 0;
// var bary = -45;
// var barz = 110
// var MINVELOCITY = 300;
// var MAXVELOCITY = 100;
// var VEL_JUMP = 25;
//
//
// function conversion(value){
//   velocity = value*-2 + 200;
//   scene.remove(scene.getObjectByName("stringVelocity"));
//   stringVelocity();
// }
//
// function stringVelocity(){
//   var fontLoader = new THREE.FontLoader();
// 	fontLoader.load('https://cdn.rawgit.com/redwavedesign/ccb20f24e7399f3d741e49fbe23add84/raw/402bcf913c55ad6b12ecfdd20c52e3047ff26ace/bebas_regular.typeface.js', function(font) {
// 		var fontMaterial = new THREE.MeshPhongMaterial({
// 			color: 'gray'
// 		});
//     var text = "x".concat((velocity-200)*-1+200);
// 		var t = new THREE.TextGeometry(text, {
// 			font: font,
// 			size: 5,
// 			height: 1,
// 			curveSegments: 2
// 		});
// 		var tm = new THREE.Mesh(t, fontMaterial);
// 		tm.position.x = -7;
// 		tm.position.y = bary+12;
// 		tm.position.z = barz+13;
//     tm.name = 'stringVelocity';
// 		scene.add(tm);
// 	});
// }
//
// function createVelocityBar(){
//
//   // BAR
//   var geometry = new THREE.CylinderGeometry( 5, 5, 100, 32 );
//   var material = new THREE.MeshBasicMaterial( {
//     color: 0xff0000,
//     transparent: true,
//     opacity: 0.7} );
//   var cylinder = new THREE.Mesh( geometry, material );
//   cylinder.position.set(0,bary,barz+10);
//   cylinder.rotation.z = Math.PI/2;
//   cylinder.name = 'vbar'
//   scene.add( cylinder );
//
//   // CURSOR
//   var geometry1 = new THREE.CylinderGeometry( 8, 8, 3, 32 );
//   var material1 = new THREE.MeshBasicMaterial( {color: 'gray'} );
//   var cursor = new THREE.Mesh( geometry1, material1 );
//   cursor.position.set(0,bary,barz+10);
//   cursor.rotation.z = Math.PI/2;
//   cursor.name = 'cursor';
//   scene.add( cursor );
// }
