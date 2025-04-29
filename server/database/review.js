const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const reviewSchema = new Schema({
  id: {
    type: Number,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  dealership: {
    type: Number,
    required: true,
  },
  review: {
    type: String,
    required: true,
  },
  purchase: {
    type: Boolean,
    default: false, // Optional
  },
  purchase_date: {
    type: String,
    default: "", // Optional
  },
  car_make: {
    type: String,
    default: "", // Optional
  },
  car_model: {
    type: String,
    default: "", // Optional
  },
  car_year: {
    type: Number,
    default: 0, // Optional
  },
});

module.exports = mongoose.model('reviews', reviewSchema);
