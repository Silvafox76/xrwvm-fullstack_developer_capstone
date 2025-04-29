/* ─────────────  Core libs  ───────────── */
const express    = require('express');
const mongoose   = require('mongoose');
const fs         = require('fs');
const cors       = require('cors');
const bodyParser = require('body-parser');

/* ─────────────  Config  ──────────────── */
const PORT      = process.env.PORT      || 3030;
const MONGO_URL = process.env.MONGO_URL || 'mongodb://mongo_db:27017/bestcar';

/* ────────────  Express app  ─────────── */
const app = express();
app.use(cors());
app.use(bodyParser.json());

/* ────────────  Load seed data  ───────── */
const reviewsSeed     = JSON.parse(fs.readFileSync('./data/reviews.json', 'utf8')).reviews;
const dealershipsSeed = JSON.parse(fs.readFileSync('./data/dealerships.json', 'utf8')).dealerships;

/* ────────────  Models  ───────────────── */
const Reviews     = require('./review');
const Dealerships = require('./dealership');

/* ────────────  Seed helper  ──────────── */
async function seedIfNeeded() {
  const count = await Dealerships.countDocuments();
  if (count) {
    console.log('ℹ️  Seed skipped (data already present)');
    return;
  }

  await Promise.all([
    Reviews.deleteMany({}),
    Dealerships.deleteMany({})
  ]);

  await Reviews.insertMany(reviewsSeed);
  await Dealerships.insertMany(dealershipsSeed);

  console.log('✅ Seed data inserted');
}

/* ─────────────  Routes  ─────────────── */
app.get('/', (_, res) => res.send('BestCars API is live ✅'));

/* --- Reviews --- */
app.get('/fetchReviews',            async (_ , res) => res.json(await Reviews.find()));
app.get('/fetchReviews/dealer/:id', async (r , res) => res.json(await Reviews.find({ dealership: +r.params.id })));

app.post('/insert_review', async (req, res) => {
  try {
    const last  = await Reviews.findOne().sort({ id: -1 }).lean();
    const next  = last ? last.id + 1 : 1;
    const saved = await Reviews.create({ id: next, ...req.body });
    res.json(saved);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

/* --- Dealerships --- */
app.get('/fetchDealers',        async (_ , res) => res.json(await Dealerships.find()));
app.get('/fetchDealers/:state', async (r , res) => res.json(await Dealerships.find({ state: r.params.state })));
app.get('/fetchDealer/:id',     async (r , res) => res.json(await Dealerships.findOne({ id: +r.params.id })));

/* ─────────────  Bootstrap  ──────────── */
(async () => {
  try {
    await mongoose.connect(MONGO_URL, { serverSelectionTimeoutMS: 10_000 });
    console.log(`✅ Connected to Mongo at ${MONGO_URL}`);
    await seedIfNeeded();

    app.listen(PORT, () => console.log(`🚀 API up on http://localhost:${PORT}`));
  } catch (err) {
    console.error('❌ Fatal start-up error:', err);
    process.exit(1);
  }
})();
