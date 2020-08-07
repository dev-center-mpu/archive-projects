const express = require('express');
const path = require('path');
const multer = require('multer');
const fs = require('fs-extra');
const Datastore = require('nedb');

const router = express();
const upload = multer({ storage: multer.memoryStorage() });
const publicFiles = path.join(__dirname, '..', '..', 'public', 'mpu-cloud-old');
const db = new Datastore({ filename: path.join(process.cwd(), 'mpu-cloud-old-data.db'), autoload: true });

db.insert({ _id: '__autoid__', value: -1 });
db.getAutoId = function (onFind) {
    db.findOne({ _id: '__autoid__' }, function (err, doc) {
        if (err) {
            onFind && onFind(err)
        } else {
            // Update and returns the index value
            db.update({ _id: '__autoid__' }, { $set: { value: ++doc.value } }, {},
                function (err, count) {
                    onFind && onFind(err, doc.value);
                });
        }
    });
    return db;
}

router.use("/", express.static(publicFiles));

router.get('/', (req, res) => res.sendFile(path.join(publicFiles, 'index.html')));

router.get('/view', function (req, res) {
    if (req.query.id) {
        res.sendFile(path.join(publicFiles, '/view.html'));
    }
});

router.get('/models', (req, res) => {
    db.find({ id: { $gte: 0 } }, (err, doc) => {
        if (err) { // Если ошибка базы данных
            res.status(500).send('Server failed!');
            throw err;
        }

        doc.forEach(element => {
            delete element.fileOrigName;
            delete element.gltfName;
            delete element._id;
        });

        res.json(doc);
    })
});

router.get('/models/:id', upload.array(), function (req, res) {
    db.findOne({ id: parseInt(req.params.id) }, (err, doc) => {
        if (err) { // Если ошибка базы данных
            res.status(500).send('Server failed!');
            throw err;
        } else if (!doc) { // Если модель в облаке не найдена
            res.status(404).send('Not Found!');
            return;
        }

        let cellPath = path.join(publicFiles, 'storage', req.params.id); // Путь к физической папке
        let bufGLTF = fs.readFileSync(path.join(cellPath, doc.gltfName));

        let responseBody = {
            id: doc.id,
            model: bufGLTF.toString('base64'),
            title: doc.title,
            author: doc.author,
            desc: doc.desc
        }

        res.json(responseBody);
    })
})

module.exports = router;
