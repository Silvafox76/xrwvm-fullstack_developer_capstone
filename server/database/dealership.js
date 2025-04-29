// server/database/dealership.js
const mongoose = require('mongoose');
const Schema   = mongoose.Schema;

const dealerSchema = new Schema({
  id:          { type: Number, required: true },
  city:        { type: String, required: true },
  state:       { type: String, required: true },
  st:          { type: String, required: true },
  address:     { type: String, required: true },
  zip:         { type: String },
  lat:         Number,
  long:        Number,
  short_name:  String,
  full_name:   String
});

module.exports = mongoose.model('dealerships', dealerSchema);
