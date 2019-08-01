var renderer, scene, camera;
var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2();
var gparent = new THREE.Object3D();
var root;
var algorithm = "PGM";
var environment;
var laststep;
var intervalID;
var counter = 0;
var controls;
var env = {};

var agent_orientation = 1;
gparent.name = "text_parent";
gparent.position.z = 50;
var hist = new Array();


var env_set = false;
var pushed = 1; //Means that text_parent is at -Math.PI/6
var epoch;



init();
animate();

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


function resetColor(array) {

  for (var i = 0; i < array.length; i++) {
    scene.getObjectByName("text_parent").getObjectByName(array[i]).material.color = new THREE.Color(0x9A9A9A);
  }
}



function init() {
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
  createAgent();
  scene.add(gparent);
  showMenu();
  stringVelocity();
  createVelocityBar();


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
  scene.getObjectByName("switch").position.z += 3;
  scene.getObjectByName("text_parent").visible = true;
  rotateObject(pushed * 2 * Math.PI / 3, 0, 0, "text_parent", 1000);
  pushed *= -1;
}

function startExperiment(){
  epoch = 0;
  agent_orientation=1;
  scene.getObjectByName("text_parent").visible = false;
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
