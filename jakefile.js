
var files = new jake.FileList();
files.include('ui/*.ui');
var interfaces = files.toArray().map(function(fileName){
    return fileName.replace('ui', '.').replace('.ui', '_ui.py');
});

var files222 = new jake.FileList();
files222.include('ui/*.qrc');
var resources = files222.toArray().map(function(fileName){
    return fileName.replace('ui', '.').replace('.qrc', '_rc.py');
});

var files5555 = new jake.FileList();
files5555.include('ui/*.svg');
var vectors = files5555.toArray();
var images = files5555.toArray().map(function(fileName){
    return fileName.replace('.svg', '.extracted');
});

rule(/_ui\.py$/, function(f){return 'ui/' + f.replace('_ui.py', '.ui')}, {async: true}, function(){
    console.log('building', this.name);
    jake.exec('D:/Projetos/xcalcs/venv/Scripts/pyside-uic -o ' + this.name + ' ' + this.source, function(){complete()});
});

rule(/_rc\.py$/, function(f){return 'ui/' + f.replace('_rc.py', '.qrc')}, {async: true}, function(){
    console.log('building', this.name);
    jake.exec('D:/Projetos/xcalcs/venv/Lib/site-packages/PySide/pyside-rcc -py3 -o ' + this.name + ' ' + this.source, function(){complete()});
});

rule(/\.extracted$/, function(f){return f.replace('.extracted', '.svg')}, {async: true}, function(){
    console.log('extracting', this.name);
    jake.exec('echo nhaca' + this.name + ' ' + this.source, function(){complete()});
});

desc('process UI files');
task('ui', interfaces, {async: true}, function(){complete()});

desc('process QRC files');
task('rc', Array().concat(resources, 'image'), {async: true}, function(){complete()});

desc('extract images from svg');
task('image', images, {async: true}, function(){complete()});
