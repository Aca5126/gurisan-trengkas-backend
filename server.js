const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const translateRouter = require('./src/routes/translate');

const app = express();

// CORS: benarkan GitHub Pages (*.github.io)
const corsOptions = {
  origin: (origin, callback) => {
    if (!origin) return callback(null, true);
    try {
      const u = new URL(origin);
      if (u.hostname.endsWith('github.io')) return callback(null, true);
    } catch {}
    return callback(null, false);
  }
};
app.use(cors(corsOptions));
app.use(bodyParser.json({ limit: '10mb' }));

app.get('/health', (req, res) => res.json({ ok: true, time: new Date().toISOString() }));
app.use('/api', translateRouter);

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
