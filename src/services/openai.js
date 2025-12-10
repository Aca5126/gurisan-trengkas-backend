const axios = require('axios');

// Nota: Isikan OPENAI_API_KEY dan OPENAI_MODEL di Render (Environment Variables).
// Contoh model: gpt-4.1 (atau model vision setara).
async function recognizeAndTranslate(imageBase64) {
  const apiKey = process.env.OPENAI_API_KEY;
  const model = process.env.OPENAI_MODEL;

  if (!apiKey || !model) {
    throw new Error('Missing OpenAI config');
  }

  // Prompt berfokus kepada Pitman 2000 Malaysia
  const systemPrompt = 'Anda ialah penterjemah Trengkas Pitman 2000 (Malaysia) ke Bahasa Melayu. Terangkan perkataan yang diwakili gurisan secara ringkas dan tepat.';
  const userPrompt = `Imej base64 gurisan trengkas (Pitman 2000 Malaysia). Huraikan perkataan yang diwakili gurisan ini: ${imageBase64}`;

  // Contoh panggilan API (sesuaikan dengan endpoint model vision semasa)
  const response = await axios.post('https://api.openai.com/v1/chat/completions', {
    model,
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt }
    ]
  }, {
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    timeout: 30000
  });

  const content = response.data?.choices?.[0]?.message?.content?.trim();
  return content || '';
}

module.exports = { recognizeAndTranslate };
