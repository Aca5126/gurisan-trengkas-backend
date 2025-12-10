const express = require('express');
const router = express.Router();
const { recognizeAndTranslate, recognizeSyllable } = require('../services/openai');

// Terjemah imej gurisan → perkataan penuh + suku kata + fonetik
router.post('/translate', async (req, res) => {
  try {
    const { imageBase64 } = req.body;
    if (!imageBase64 || typeof imageBase64 !== 'string' || !imageBase64.startsWith('data:image')) {
      return res.status(400).json({ error: 'Image data (base64) diperlukan' });
    }
    const result = await recognizeAndTranslate(imageBase64);
    res.json(result); // { perkataan, sukuKata[], fonetik }
  } catch (err) {
    console.error('Error /api/translate:', err?.response?.data || err.message);
    res.status(500).json({ error: 'Translation failed' });
  }
});

// Ramal suku kata untuk gurisan tunggal (+ fonetik)
router.post('/suku-kata', async (req, res) => {
  try {
    const { imageBase64 } = req.body;
    if (!imageBase64 || typeof imageBase64 !== 'string' || !imageBase64.startsWith('data:image')) {
      return res.status(400).json({ error: 'Image data (base64) diperlukan' });
    }
    const result = await recognizeSyllable(imageBase64);
    res.json(result); // { sukuKata, fonetik }
  } catch (err) {
    console.error('Error /api/suku-kata:', err?.response?.data || err.message);
    res.status(500).json({ error: 'Syllable failed' });
  }
});

module.exports = router;
