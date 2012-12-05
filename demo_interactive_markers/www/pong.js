(function(THREE) {

  var container;
  var camera, cameraControls, scene0, scene1, hoverScene, renderer;
  var pickingData = [], pickingTexture, pickingScene;
  var objects = [];
  var highlightBox;

  var directionalLight;

  var mouseHandler;

  var mouse = new THREE.Vector2(), offset = new THREE.Vector3(10, 10, 10);

  init();
  animate();

  var INTERSECTED, INTERSECTION, DRAGGING;

  var imc, imm;

  var hoverObjs = [];

  function init() {

    // ////////////////////////////////////////////////

    container = document.getElementById("container");

    // setup camera
    camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.01, 1000);
    camera.position.x = 3;
    camera.position.y = 3;
    camera.position.z = 3;

    projector = new THREE.Projector();

    // setup scene
    scene0 = new THREE.Scene();
    scene1 = new THREE.Scene();

    // setup camera mouse control
    cameraControls = new THREE.RosOrbitControls(camera);
    cameraControls.zoomOut(6);

    // add lights
    scene0.add(new THREE.AmbientLight(0x555555));
    directionalLight = new THREE.DirectionalLight(0xffffff);

    // attach light to camera
    scene0.add(directionalLight);

    var ros = new ROS('ws://'+document.domain+':9090');


    imc = new InteractiveMarkers.Client(ros);
    imm = new THREE.InteractiveMarkerManager(scene0, imc);
    imc.subscribe('/pong');

    renderer = new THREE.WebGLRenderer({
      antialias : false
    });

    renderer.setClearColorHex(0x333333, 1.0);
    renderer.sortObjects = false;
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMapEnabled = false;
    renderer.autoClear = false;
    renderer.setFaceCulling(0);

    container.appendChild(renderer.domElement);

    renderer.domElement.addEventListener('contextmenu', function(event) {
      event.preventDefault();
    }, false);

    mouseHandler = new THREE.MouseHandler(renderer, camera, scene0, cameraControls);

    mouseHandler.addEventListener("mouseover", onMouseOver);
    mouseHandler.addEventListener("mouseout", onMouseOut);
  }

  function animate() {
    requestAnimationFrame(animate);
    render();
  }

  function onMouseOver(event) {
    hoverObjs.push(event.currentTarget);
  }

  function onMouseOut(event) {
    hoverObjs.splice(hoverObjs.indexOf(event.currentTarget), 1);
  }

  function render() {
    cameraControls.update();

    // put light to the top-left of the camera
    directionalLight.position = camera.localToWorld(new THREE.Vector3(-1, 1, 0));
    directionalLight.position.normalize();

    renderer.clear(true, true, true);
    renderer.render(scene0, camera);

    INTERACT3D.renderHighlight(renderer, scene0, camera, hoverObjs);

    // clear depth & stencil & render overlay scene
    //renderer.clear(false, true, true);
    renderer.render(scene1, camera);
  }

})(THREE);