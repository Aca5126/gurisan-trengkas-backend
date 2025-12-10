const axios = require('axios');

// Nota: Isi OPENAI_API_KEY dan OPENAI_MODEL di Render.
// OPENAI_MODEL hendaklah model vision/chat yang menyokong imej.

function buildHeaders() {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) throw new Error('Missing OpenAI API key');
  return {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  };
}

async function callModel(messages) {
  const model = process.env.OPENAI_MODEL;
  if (!model) throw new Error('Missing OpenAI model');
  const response = await axios.post('https://api.openai.com/v1/chat/completions', {
    model,
    messages
  }, { headers: buildHeaders(), timeout: 30000 });
  return response.data?.choices?.[0]?.message?.content?.trim() || '';
}

// Terjemah imej → perkataan penuh + suku kata + fonetik
async function recognizeAndTranslate(imageBase64) {
  const systemPrompt = 'Anda ialah penterjemah Trengkas Pitman 2000 (Malaysia) ke Bahasa Melayu. Kenal pasti perkataan penuh, pecahkan kepada suku kata, dan berikan transkripsi fonetik ringkas (IPA). Jika imej mengandungi lebih daripada satu gurisan, anggap ia perkataan/ayat dengan beberapa suku kata.';
  const userPrompt = `Imej gurisan trengkas (base64) berikut mewakili perkataan/ayat. Kembalikan dalam format ketat:
Perkataan: <perkataan penuh>
SukuKata: <suku kata berurutan dipisah dengan tanda +>
Fonetik: <IPA>

Imej: ${imageBase64}`;

  const content = await callModel([
    { role: 'system', content: systemPrompt },
    { role: 'user', content: userPrompt }
  ]);

  // Contoh output dijangka:
  // Perkataan: mari ke sekolah
  // SukuKata: ma + ri + ke + se + ko + lah
  // Fonetik: /ma.ri ke sə.kolah/
  const perkataanMatch = content.match(/Perkataan:\s*([^\n]+)/i);
  const sukuMatch = content.match(/SukuKata:\s*([^\n]+)/i);
  const fonetikMatch = content.match(/Fonetik:\s*([^\n]+)/i);

  const perkataan = perkataanMatch ? perkataanMatch[1].trim() : '';
  const sukuRaw = sukuMatch ? sukuMatch[1].trim() : '';
  const sukuKata = sukuRaw ? sukuRaw.split(/\s*\+\s*/).map(s => s.trim()).filter(Boolean) : [];
  const fonetik = fonetikMatch ? fonetikMatch[1].trim() : '';

  return { perkataan, sukuKata, fonetik };
}

// Ramal suku kata tunggal + fonetik
async function recognizeSyllable(imageBase64) {
  const systemPrompt = 'Anda ialah pakar Trengkas Pitman 2000 (Malaysia). Berdasarkan imej gurisan tunggal, teka suku kata yang paling mungkin dan berikan transkripsi fonetik ringkas (IPA).';
  const userPrompt = `Format ketat:
SukuKata: <suku kata>
Fonetik: <IPA>

Imej: ${imageBase64}`;

  const content = await callModel([
    { role: 'system', content: systemPrompt },
    { role: 'user', content: userPrompt }
  ]);

  const sukuMatch = content.match(/SukuKata:\s*([^\n]+)/i);
  const fonetikMatch = content.match(/Fonetik:\s*([^\n]+)/i);
  const sukuKata = sukuMatch ? sukuMatch[1].trim() : content.trim();
  const fonetik = fonetikMatch ? fonetikMatch[1].trim() : '';
  return { sukuKata, fonetik };
}

module.exports = { recognizeAndTranslate, recognizeSyllable };
