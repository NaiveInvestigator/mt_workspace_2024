
"use strict";

let Gprmc = require('./Gprmc.js');
let GpgsvSatellite = require('./GpgsvSatellite.js');
let Gpgst = require('./Gpgst.js');
let Sentence = require('./Sentence.js');
let Gpgsa = require('./Gpgsa.js');
let Gpgsv = require('./Gpgsv.js');
let Gpgga = require('./Gpgga.js');

module.exports = {
  Gprmc: Gprmc,
  GpgsvSatellite: GpgsvSatellite,
  Gpgst: Gpgst,
  Sentence: Sentence,
  Gpgsa: Gpgsa,
  Gpgsv: Gpgsv,
  Gpgga: Gpgga,
};
