var express = require('express');
var app = express();
var server = require('http').createServer(app);
var socket = require('socket.io');

app.use(express.static(__dirname + '/public'));

app.get('/', function(req, res, next) {
    res.sendFile(__dirname + '/public/index.html');
});

var io = socket.listen(server);

io.sockets.on('connection', function(client) {

    require('./src/file_upload')(client);
    require('./src/img_generator')(client);

});

server.listen(4200);