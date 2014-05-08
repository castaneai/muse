var fs = require('fs');
var mm = require('musicmetadata');


var parser = mm(fs.createReadStream('s.mp3'));
parser.on('metadata', function(metadata) {
    console.log(metadata)
});