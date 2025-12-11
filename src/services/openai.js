const axios = require('axios');

function buildHeaders() {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) throw new Error('Missing OpenAI API key');
  return {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  };
}

async function callModelVision(messages) {
  const model = process.env.OPENAI_MODEL || 'gpt-4o-mini';
  const url = 'https://api.openai.com/v1/chat/completions';
  const resp = await axios.post(
    url,
    { model, messages },
    { headers: buildHeaders(), timeout: 90000 }
  );
  return (resp.data?.choices?.[0]?.message?.content || '').trim();
}

function normalizeDataText(text) {
  const perkataanMatch = text.match(/Perkataan:\s*([^\n]+)/i);
  const sukuMatch = text.match(/SukuKata:\s*([^\n]+)/i);
  const fonetikMatch = text.match(/Fonetik:\s*([^\n]+)/i);

  const perkataan = perkataanMatch ? perkataanMatch[1].trim() : '';
  const sukuRaw = sukuMatch ? sukuMatch[1].trim() : '';
  const sukuKata = sukuRaw
    ? sukuRaw.split(/\s*\+\s*/).map(s => s.trim()).filter(Boolean)
    : [];
  const fonetik = fonetikMatch ? fonetikMatch[1].trim() : '';

  return { perkataan, sukuKata, fonetik };
}

async function recognizeAndTranslate(imageBase64, target) {
  const systemPrompt =
    'Anda ialah penterjemah Trengkas Pitman 2000 (Malaysia) ke Bahasa Melayu. ' +
    'Kenal pasti perkataan penuh, pecahkan kepada suku kata, dan berikan transkripsi fonetik ringkas (IPA). ' +
    'Balas tepat format yang diminta.';

  const userPromptText =
`Imej gurisan trengkas berikut mewakili perkataan/ayat.
Jika sesuai, bandingkan dengan sasaran: "${(target || '').trim()}".

Balas dalam format ketat:
Perkataan: <perkataan penuh>
SukuKata: <suku kata berurutan dipisah dengan tanda +>
Fonetik: <IPA>`;

  const messages = [
    { role: 'system', content: systemPrompt },
    {
      role: 'user',
      content: [
        { type: 'text', text: userPromptText },
        {
          type: 'image_url',
          image_url: {
            url: imageBase64
          }
        }
      ]
    }
  ];

  try {
    const content = await callModelVision(messages);
    return normalizeDataText(content);
  } catch (e) {
    console.error('recognizeAndTranslate error:', e.message);
    if (e.message?.includes('maximum context length')) {
      return { error: 'Imej terlalu besar. Sila kecilkan kanvas atau kurangkan lorekan.' };
    }
    return { error: 'Gagal memproses imej' };
  }
}

async function recognizeSyllable(imageBase64) {
  const systemPrompt =
    'Anda ialah pakar Trengkas Pitman 2000 (Malaysia). ' +
    'Berdasarkan imej gurisan tunggal, teka suku kata yang paling mungkin dan berikan IPA ringkas. ' +
    'Balas tepat format yang diminta.';

  const userPromptText =
`Format ketat:
SukuKata: <suku kata>
Fonetik: <IPA>`;

  const messages = [
    { role: 'system', content: systemPrompt },
    {
      role: 'user',
      content: [
        { type: 'text', text: userPromptText },
        {
          type: 'image_url',
          image_url: {
            url: imageBase64
          }
        }
      ]
    }
  ];

  try {
    const content = await callModelVision(messages);
    const sukuMatch = content.match(/SukuKata:\s*([^\n]+)/i);
    const fonetikMatch = content.match(/Fonetik:\s*([^\n]+)/i);
    const sukuKata = sukuMatch ? sukuMatch[1].trim() : content.trim();
    const fonetik = fonetikMatch ? fonetikMatch[1].trim() : '';
    return { sukuKata, fonetik };
  } catch (e) {
    console.error('recognizeSyllable error:', e.message);
    return { error: 'Gagal memproses imej' };
  }
}

module.exports = {
  recognizeAndTranslate,
  recognizeSyllable
};
