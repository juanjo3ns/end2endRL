var maxHealth = 4;
var prevHealth = 0;
var scale_ = 1;
var health;

function createLife() {
  // EXTERIOR BALL
  health = new THREE.Object3D();
  health.name = "health";
  var geometry = new THREE.SphereGeometry(maxHealth, 32, 32, 0, 6.3, 0, 3.4);
  var material = new THREE.MeshBasicMaterial({
    color: 0xFFFFFF,
    transparent: true,
		opacity: 0.5
  });
  var capsule = new THREE.Mesh(geometry, material);
  capsule.position.set(0,14,0);
  capsule.name = 'capsule';
  health.add(capsule);

  // INTERIOR BALL
  var geometry1 = new THREE.SphereGeometry(maxHealth, 32, 32, 0, 6.3, 0, 3.4);
  var material1 = new THREE.MeshBasicMaterial({
    color: 'green'
  });
  var life = new THREE.Mesh(geometry1, material1);
  life.position.set(0,14,0);
  life.name = 'life';
  health.add(life);
  scene.add(health);
}

function lifeColor(value){
  return [1-value, value];
}

function reduceLife(health){
  health = health/scale_*maxHealth;
  if (health < 0){
    removeHealthIndicators();
  }else{
    if (health > maxHealth){
      health = maxHealth;
    }
    color = health/maxHealth;
    reduce = health/prevHealth;
    scene.getObjectByName("health").getObjectByName("life").geometry.scale(reduce,reduce,reduce);
    scene.getObjectByName("health").getObjectByName("life").material.color = new THREE.Color( lifeColor(color)[0], lifeColor(color)[1], 0 )
    prevHealth = health;
  }
}

function setMaxHealth(value){
  scale_ = value;
  prevHealth = maxHealth;
}

function removeHealthIndicators(){
  scene.remove(scene.getObjectByName("health"));
}
