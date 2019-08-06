var x = -55; y = -25; z = 50;
var envs = new Array("easy", "medium", "hard");

function showMenu() {
	// """SWITCH TO SHOW AND HIDE WHOLE MENU"""
	var sw_b = new THREE.BoxGeometry(11, 10, 11);
	var material_b = new THREE.MeshPhongMaterial({
		color: 'grey',
		flatShading: THREE.FlatShading
	});
	var swch = new THREE.Mesh(sw_b, material_b);
	swch.position.x = x-20;
	swch.position.y = y;
	swch.position.z = 50+z;
	var geometry = new THREE.CylinderGeometry( 4, 4, 10, 16 );
	var material = new THREE.MeshBasicMaterial( {color: 0xff0000} );
	var cylinder = new THREE.Mesh( geometry, material );
	var edges = new THREE.EdgesGeometry(geometry);
	var line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({
		color: 'black'
	}));
	cylinder.add(line);
	cylinder.name = "switch";
	cylinder.position.x = x-20;
	cylinder.position.y = y;
	cylinder.position.z = 55+z;
	cylinder.rotation.x = Math.PI/2;
	scene.add( cylinder );
	scene.add(swch);
	// """-------------------------------------"""

	// """TEXT FOR ENVIRONMENTS"""
	var fontLoader = new THREE.FontLoader();
	fontLoader.load('https://cdn.rawgit.com/redwavedesign/ccb20f24e7399f3d741e49fbe23add84/raw/402bcf913c55ad6b12ecfdd20c52e3047ff26ace/bebas_regular.typeface.js', function (font) {
		var fontMaterial = new THREE.MeshPhongMaterial({
			color: 'black'
		});
		for (var j = 0; j < 3; j++) {
			var t = new THREE.TextGeometry(envs[j], {
				font: font,
				size: 5,
				height: 1,
				curveSegments: 2
			});
			var m = new THREE.Mesh(t, fontMaterial);
			m.position.x = x + 20 +j * 35;
			m.position.y = y - 23;
			m.position.z = z+6;
			gparent.add(m);
		}

	});
	// """BUTTONS TO SELECT ENVIRONMENT"""
	for (var j = 0; j < 3; j++) {
		var box = new THREE.BoxGeometry(8, 8, 2);
		var material = new THREE.MeshPhongMaterial({
			color: 'gray',
			flatShading: THREE.FlatShading
		});
		var mesh = new THREE.Mesh(box, material);
		mesh.name = envs[j];
		mesh.position.x = x + 10 + j * 37;
		mesh.position.y = y-20;
		mesh.position.z = z+6;

		gparent.add(mesh);
	}
	var sw_b = new THREE.BoxGeometry(110, 25, 2);
	var mt = new THREE.MeshPhongMaterial({
		color: 'white',
		flatShading: THREE.FlatShading
	});
	var block1 = new THREE.Mesh(sw_b, mt);
	var sw_b = new THREE.BoxGeometry(110, 25, 2);
	block1.position.set(0, y-20, z+1);
	gparent.add(block1);
	gparent.rotation.x = -Math.PI/6;

}
