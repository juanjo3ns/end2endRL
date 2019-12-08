var renderer, scene, camera;
var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2();
var agents = new THREE.Object3D();
var root;
var algorithm = "GA";
var environment;

agents.name = "agents";
var intervalID;
var env = {};
var counter = 0;
var cells;
var cell_dimension = 10;
var ini_x,ini_z, height, width;
var velocity = 150;

var env_set = false;
var intervals = {};
var deads;
var epoch;
var version;
var orientations;

init();
animate();


function init() {
  var url_string = window.location.href;
  var url = new URL(url_string);
  version = url.searchParams.get("version");
  console.log(version);
  renderer = new THREE.WebGLRenderer({
    antialias: true
  });
  var width = window.innerWidth;
  var height = window.innerHeight;

  renderer.setSize(width, height);
  renderer.setClearColor('#151515', 1);
  document.body.appendChild(renderer.domElement);

  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(55, width / height, 1, 10000);
  camera.position.set(0, 85, 250);
  camera.name = "camera";
  scene.add(camera)

  //LIGHTNING
  light = new THREE.PointLight(0xffffff, 1, 4000);
  light.position.set(100, 100, -150);
  light_two = new THREE.PointLight(0xffffff, 1, 4000);
  light_two.position.set(-100, 100, -50);
  lightAmbient = new THREE.AmbientLight('white');
  scene.add(light, light_two, lightAmbient);

  // OBJECTS
  loadEnvironment(algorithm, version, counter);
  if (intervals[environment] == undefined){
		intervals[environment] = new Array(env["numAgents"]);
	}
  generateBoard();
  // stringVelocity();
  // createVelocityBar();
  counter = 1;
  createAgents(iterations);

  document.addEventListener('click', onDocumentMouseDown, false);
  controls = new THREE.OrbitControls(camera, renderer.domElement);
  window.addEventListener('resize', onWindowResize, false);
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.updateProjectionMatrix();
};


function resetEnvironment(){

  for (var i=0;i<intervals[environment].length;i++){
    clearInterval(intervals[environment][i]);
  }
  removeAgents();
}


function animate() {
  requestAnimationFrame(animate);
  controls.update();
  TWEEN.update();
  render();
}

function render() {
  renderer.render(scene, camera);

}
