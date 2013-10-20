var app = require('http').createServer(handler)
  , io = require('socket.io').listen(app)
  , fs = require('fs')
  , net = require('net')

app.listen(9111);

function handler(req, res) {
    fs.readFile(__dirname + '/index.html', function (err, data) {  
        res.writeHead(200);
        res.end(data);
    });
}

browser = null;
io.set('log level', 1);
io.sockets.on('connection', function (socket) { browser = socket });

thinkgear = net.connect(13854, '127.0.0.1', function() {
    thinkgear.write(JSON.stringify({enableRawOutput: true, format: 'Json'}));
});

buffer = "";
thinkgear.on('data', function(data) {
    buffer += data.toString();
    var packets = buffer.split('\r');
    if (packets.length == 0) return;
    buffer = packets.pop();
    for (var i in packets) {
        var packet = JSON.parse(packets[i]);
        if (packet.hasOwnProperty('rawEeg') && browser) {
            browser.emit('eeg', packet['rawEeg']);
        }
    }
});