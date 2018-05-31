
function blockUI() {
    blockedUI = true;
    $.blockUI({
        message: '<span id="canvasloader-container"></span>' + '',
        fadeIn: 0,
        fadeOut: 0,
        baseZ: 9999,
        css: {
            border: 'none',
            backgroundColor: 'transparent',
            color: '#fff'//,
        },
        overlayCSS: {
            backgroundColor: '#000',
            opacity: 0.25
        }
    });
    createLoader("canvasloader-container", 60);
}

function createLoader(elementId, diameter) {
    var cl = new CanvasLoader('canvasloader-container');
    cl.setColor('#ffffff'); // default is '#000000'
    cl.setShape('roundRect'); // default is 'oval'
    cl.setDiameter(diameter); // default is 40
    cl.setDensity(15); // default is 40
    cl.setRange(0.8); // default is 1.3
    cl.setSpeed(1); // default is 2
    cl.setFPS(24); // default is 24
    cl.show(); // Hidden by default
}

function unblockUI() {
    blockedUI = false;
    $.unblockUI();
}
