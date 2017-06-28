var fs = require('fs');
var UIDGenerator = require('uid-generator');

module.exports = function (client) {

    var files = [];
    var blockSize = 524288;

    client.on('Upload.Start', function (data) {

        var fileToken = new UIDGenerator(128, UIDGenerator.BASE62).generateSync();
        var exchangeToken = new UIDGenerator(128, UIDGenerator.BASE62).generateSync();
        var filePath = 'temp/' + fileToken;

        files[exchangeToken] = {
            fileSize: data.size,
            data: "",
            downloaded: 0,
            filePath: filePath,
            fileToken: fileToken
        };

        fs.open(filePath, "a", 0755, function (err, fd) {
            if (err)
                throw err;

            files[exchangeToken].handler = fd;
            client.emit('Upload.RequestData', {cursor: 0, blockSize: blockSize, token: exchangeToken});
        });
    });

    client.on('Upload.Data', function (data) {

        var token = data.token;
        files[token].downloaded += data.data.length;
        files[token].data += data.data;

        if (files[token].downloaded > files[token].fileSize) {
            client.emit('Upload.Done', {
                token: token,
                error: 'More data than the file size was received'
            });
        }
        else if (files[token].downloaded === files[token].fileSize)
        {
            fs.write(files[token].handler, files[token].data, null, 'Binary', function (err, callkack) {
                if (err)
                    throw err;

                client.emit('Upload.Done', {token: token, fileToken: files[token].fileToken});
            });
        }
        else if (files[token].data.length > 10485760) {
            fs.write(files[token].handler, files[token].data, null, 'Binary', function (err, callback) {
                if (err)
                    throw err;

                files[token].data = "";
                client.emit('Upload.RequestData', {
                    cursor: files[token].downloaded,
                    blockSize: blockSize,
                    token: token
                });
            });
        }
        else {
            client.emit('Upload.RequestData', {
                cursor: files[token].downloaded,
                blockSize: blockSize,
                token: token
            });
        }
    });
};