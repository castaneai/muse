var express = require('express');
var app = express();


app.get('/musics/', function() {
    console.log('ｳｪｲ');
});

app.listen(3000);