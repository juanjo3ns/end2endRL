var renderer, scene, camera;
var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2();
var root;
var algorithm = "A2C";
var environment;
var laststep;
var intervalID;
var counter = 0;
var controls;
var env = {};
var velocity = 150;

var agent_orientation = 1;
var hist = new Array();


var env_set = false;
var epoch;
var version;



init();
animate();

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}



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
  camera.position.set(0, 85, 270);
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
  createAgent(startExperiment);
  generateBoard();
  // stringVelocity();
  // createVelocityBar();
  // startExperiment();


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

  clearInterval(intervalID);
  agent_orientation=1;
  epoch = 0;
  removeHealthIndicators();
  scene.getObjectByName("agent").rotation.y = 0;
  scene.getObjectByName("agent").visible = false;
}

function startExperiment(){
  epoch = 0;
  agent_orientation=1;
  scene.getObjectByName("agent").visible = true;
  iterations();
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
