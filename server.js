const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const translateRouter = require('./src/routes/translate');

const app = express();

// CORS: benarkan GitHub Pages (apa-apa subdomain .github.io)
const corsOptions = {
  origin: (origin, callback) => {
    // Benarkan jika tiada origin (contoh: tools online) atau berasal dari *.github.io
    if (!origin) return callback(null, true);
    try {
      const u = new URL(origin);
      if (u.hostname.endsWith('github.io')) return callback(null, true);
    } catch {}
    // Anda boleh tambah domain lain jika perlu:
    // if (origin === 'https://gurisan-trengkas-frontend.onrender.com') return callback(null, true);
    return callback(null, false);
  }
};
app.use(cors(corsOptions));

app.use(bodyParser.json({ limit: '10mb' }));

app.get('/health', (req, res) => {
  res.json({ ok: true, time: new Date().toISOString() });
});

app.use('/api/translate', translateRouter);

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
