const express = require('express');
const path = require('path');

const router = express.Router();
const publicFiles = path.join(__dirname, '..', '..', 'public', 'portfolio');

router.use('/', express.static(publicFiles));
router.get('/', (req, res) => res.sendFile(path.join(publicFiles, 'index.html')));

module.exports = router;
