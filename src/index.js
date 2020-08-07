const express = require('express');
const path = require('path');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const portfolio = require('./routes/portfolio');
const truckForge = require('./routes/truck-forge');
const ietmForgeOld = require('./routes/ietm-forge-old');
const {PORT} = require(process.cwd() + '/config.json');

const app = express();

app.use(cors());
app.use(cookieParser());

app.use('/', portfolio);
app.use('/truck-forge', truckForge);
app.use('/ietm-forge-old', ietmForgeOld);

app.listen(PORT, () => console.log(`Сервер запущен. Используемый порт: ${PORT}.`));
