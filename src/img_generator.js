var childprocess = require('child_process');

module.exports = function (client) {

    client.on('Img.Generate.Start', function (data) {

        childprocess.exec('bash src/img_verification.sh' + ' temp/' + data.fileToken, function (err, stdout, stderr) {
            if (err)
                throw err;

            if (stdout.trim() === 'OK') {

                var params = '';

                if (data.pencil)
                    params += ' --pencil';
                if (data.cartoon)
                    params += ' --cartoon';
                if (data.gray)
                    params += ' --gray';
                if (data.sepia)
                    params += ' --sepia';
                if (data.darker)
                    params += ' --darker';
                if (data.thermic)
                    params += ' --thermic';

                childprocess.exec('opencv/dist/filters' + ' -i temp/' + data.fileToken + ' -o public/out/' + data.fileToken + '.jpg' + params, function (err, stdout, stderr) {
                    if (err)
                        throw err;

                    // childprocess.exec('opencv/dist/resizing' + ' -i public/out/' + data.fileToken + ' -o public/out/' + data.fileToken + '.jpg' + ..., function (err, stdout, stderr) {
                    //     if (err)
                    //         throw err;


                    client.emit('Img.Generate.Done', {filePath: 'out/' + data.fileToken + '.jpg'});

                    // });

                });

            }
            else if (stdout.trim() === 'INVALID FORMAT') {
                client.emit('Img.Generate.Done', {
                    fileToken: data.fileToken,
                    error: 'Uploaded file is not a picture'
                });
            }

        });

    });
};