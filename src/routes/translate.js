const express = require('express');
const router = express.Router();
const { recognizeAndTranslate } = require('../services/openai');

router.post('/', async (req, res) => {
  try {
    const { imageBase64 } = req.body;
    if (!imageBase64 || typeof imageBase64 !== 'string' || !imageBase64.startsWith('data:image')) {
      return res.status(400).json({ error: 'Image data (base64) diperlukan' });
    }
    const translation = await recognizeAndTranslate(imageBase64);
    res.json({ translation });
  } catch (err) {
    console.error('Error /api/translate:', err?.response?.data || err.message);
    res.status(500).json({ error: 'Translation failed' });
  }
});

module.exports = router;
