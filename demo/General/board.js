var cells;
var surface;
var padding;
var walls;
var finalStates;
var cell_dimension = 10;
var ini_x,ini_z, height, width;

function colorTransform(value){
  var norm = 0;
  var unit = env["max_wall"]-env["min_wall"];
  if (unit!==0){
    norm = (value - env["min_wall"])/unit;
  }
  return [1-norm, norm]
}

function resetColours(){
  surf_children = scene.getObjectByName("cells").getObjectByName("surface").children;
  padd_children = scene.getObjectByName("cells").getObjectByName("padding").children;
  for(var i=0;i<surf_children.length;i++){
    scene.getObjectByName("cells").getObjectByName("surface").children[i].material.color = new THREE.Color(0x000000);
  }
  for(var i=0;i<padd_children.length;i++){
    scene.getObjectByName("cells").getObjectByName("padding").children[i].material.color = new THREE.Color("rgb(0, 26, 26)");
  }
}

function getWallMaterial(index) {
    value = env["wallValues"][index];
    var size = parseInt(Math.abs(value)*10);
    var cell = new THREE.BoxGeometry(size,size,size);

    var material = new THREE.MeshPhongMaterial({
        color: new THREE.Color( colorTransform(value)[0], colorTransform(value)[1], 0 )
    });
    return [cell, material]
}

function addWall(i,j,index){
  wall = getWallMaterial(index);
  cell = wall[0];
  material = wall[1];
  var edges = new THREE.EdgesGeometry(cell);
  var line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({color: 'black' }));
  var b = new THREE.Mesh(cell, material);
  b.name = 'l'+(j + i * (width-1)).toString();
  b.position.x = ini_x + i * cell_dimension;
  b.position.y = 5;
  b.position.z = ini_z + j * cell_dimension;
  b.add(line);
  return b;
}
function addSurface(i,j){
  var boardCell = new THREE.BoxGeometry(10, 2, 10);
  var boardMaterial = new THREE.MeshPhongMaterial({
      color: 'black',
      flatShading: THREE.FlatShading
  });
  var edges = new THREE.EdgesGeometry(boardCell);
  var line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({
    color: 'black'
  }));
  var board = new THREE.Mesh(boardCell, boardMaterial);
  board.name = i.toString()+'-'+j.toString();
  board.position.x = ini_x + i * cell_dimension;
  board.position.y = 0;
  board.position.z = ini_z + j * cell_dimension;
  board.add(line);
  return board;
}
function addPadding(i,j){
  var boardCell = new THREE.BoxGeometry(10, 2, 10);
  var boardMaterial = new THREE.MeshPhongMaterial({
      color: new THREE.Color("rgb(0, 26, 26)"),
      flatShading: THREE.FlatShading
  });
  var edges = new THREE.EdgesGeometry(boardCell);
  var line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({
    color: 'black'
  }));
  var board = new THREE.Mesh(boardCell, boardMaterial);
  board.name = i.toString()+'-'+j.toString();
  board.position.x = ini_x + i * cell_dimension;
  board.position.y = 0;
  board.position.z = ini_z + j * cell_dimension;
  board.add(line);
  return board;
}
function addFinalState(i,j){
  var cell = new THREE.BoxGeometry(10, 2, 10);
  var material = new THREE.MeshPhongMaterial({
      color: 'white',
      flatShading: THREE.FlatShading
  });
  var edges = new THREE.EdgesGeometry(cell);
  var line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({
    color: 'black'
  }));
  var b = new THREE.Mesh(cell, material);
  b.name = 'f'+(j + i * (width-1)).toString();
  b.position.x = ini_x + i * cell_dimension;
  b.position.y = 1;
  b.position.z = ini_z + j * cell_dimension;
  b.add(line);
  return b;
}


function showBoard() {
    if (scene.getObjectByName("cells")){
      scene.remove(scene.getObjectByName("cells"));
    }
    var wall_index = 0;
    height = env["height"];
    width = env["width"];
    cells = new THREE.Object3D();
    surface = new THREE.Object3D();
    finalStates = new THREE.Object3D();
    padding = new THREE.Object3D();
    walls = new THREE.Object3D();
    cells.name = 'cells';
    surface.name ='surface';
    walls.name = 'walls';
    padding.name ='padding';

    ini_x = -height*cell_dimension/2 + cell_dimension/2;
    ini_z = -width*cell_dimension/2 + cell_dimension/2;
    for (var i = 0; i < height; i++) {
        for (var j = 0; j < width; j++) {
            if ((i!=0 && i!=height-1) && (j!=0 && j!=width-1)){
              surface.add(addSurface(i,j));
            }
            if (env["wallStates"].indexOf(JSON.stringify([i, j])) != -1) {
              walls.add(addWall(i,j,wall_index));
              wall_index+=1;
            } else if (env["finalStates"].indexOf(JSON.stringify([i, j])) != -1) {
              finalStates.add(addFinalState(i,j));
            } else if (env["paddingStates"].indexOf(JSON.stringify([i, j])) != -1){
              padding.add(addPadding(i,j));
            }
        }
    }
    cells.add(surface);
    cells.add(walls);
    cells.add(finalStates);
    cells.add(padding);
    scene.add(cells);
}

function generateBoard(algorithm, environment) {
    showBoard();
}
