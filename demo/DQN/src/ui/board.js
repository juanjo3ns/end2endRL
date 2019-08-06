function colorTransform(value){
  var min = -1;
  var unit = 1.2;
  var norm = (value - min)/unit;
  return [1-norm, norm]
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
  b.position.y = 3;
  b.position.z = ini_z + j * cell_dimension;
  b.add(line);
  return b;
}


function showBoard() {
    var wall_index = 0;
    height = env["height"];
    width = env["width"];
    cells = new THREE.Object3D();
    cells.name = 'cells';
    ini_x = -height*cell_dimension/2 + cell_dimension/2;
    ini_z = -width*cell_dimension/2 + cell_dimension/2;
    for (var i = 0; i < height; i++) {
        for (var j = 0; j < width; j++) {
            if ((i!=0 && i!=height-1) && (j!=0 && j!=width-1)){
              cells.add(addSurface(i,j));
            }
            if (env["wallStates"].indexOf(JSON.stringify([i, j])) != -1) {
                cells.add(addWall(i,j,wall_index));
                wall_index+=1;
            } else if (env["finalStates"].indexOf(JSON.stringify([i, j])) != -1) {
                cells.add(addFinalState(i,j));
            } else if (env["paddingStates"].indexOf(JSON.stringify([i, j])) != -1){
                cells.add(addPadding(i,j));
            }
        }
    }
    scene.add(cells);
}

function generateBoard(algorithm, environment) {
    loadEnvironment(algorithm, environment);
    showBoard();
}
