const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const translateRouter = require('./src/routes/translate');

const app = express();

// CORS: guna ALLOWED_ORIGINS (dipisah koma) + *.github.io
const allowed = (process.env.ALLOWED_ORIGINS || '')
  .split(',')
  .map(s => s.trim())
  .filter(Boolean);

const corsOptions = {
  origin: (origin, callback) => {
    if (!origin) return callback(null, true);
    try {
      const u = new URL(origin);
      const okEnv = allowed.includes(u.origin) || allowed.includes(u.hostname);
      const okGithub = u.hostname.endsWith('github.io');
      if (okEnv || okGithub) return callback(null, true);
    } catch {
      // ignore parse error
    }
    return callback(null, false);
  }
};

app.use(cors(corsOptions));
app.use(bodyParser.json({ limit: '10mb' }));

app.get('/health', (req, res) => {
  res.json({ ok: true, time: new Date().toISOString() });
});

app.use('/api', translateRouter);

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server berjalan pada port ${PORT}`);
});
