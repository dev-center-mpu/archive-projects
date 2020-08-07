const express = require('express');
const path = require('path');
const request = require('request').defaults({
    baseUrl: 'https://developer.api.autodesk.com'
});

const router = express.Router();
const publicFiles = path.join(__dirname, '..', '..', 'public', 'truck-forge');

let expireTime = Date.now();
let token = '';

let options = {
    method: 'POST',
    url: '/authentication/v1/authenticate',
    headers: {
        'content-type': 'application/x-www-form-urlencoded'
    },
    form: {
        client_id: 'MSKuogyPaWygG9PQAMGBQK1fIoAbd3ES',
        client_secret: '6esaVpljx0GL4QL9',
        grant_type: 'client_credentials',
        scope: 'data:read'
    }
};

router.get('/auth', (req, res) => {
    if (!token || Date.now() > expireTime) {
        request(options, (e, r, body) => {
            token = body;
            expireTime = Date.now() + JSON.parse(body).expires_in;
            res.send(token);
        });
    } else {
        res.send(token);
    }
});

router.use('/', express.static(publicFiles));
router.get('/', (req, res) => res.sendFile(path.join(publicFiles, 'index.html')));

module.exports = router;
