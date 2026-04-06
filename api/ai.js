/**
 * Vercel Serverless Function: Gemini API Proxy
 * APIキーをサーバーサイドで管理し、クライアントから隠蔽します。
 */

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { prompt, image, mask } = req.body;
  const apiKey = process.env.GEMINI_API_KEY;

  if (!apiKey) {
    return res.status(500).json({ error: 'GEMINI_API_KEY is not set in environment variables.' });
  }

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;

    const parts = [
      { text: prompt },
      { inlineData: { mimeType: "image/png", data: image } }
    ];

    if (mask) {
      parts.push({ text: "Below is the mask image. The red colored areas indicate the objects to be removed or replaced. Please fill them naturally based on the background context of the first image." });
      parts.push({ inlineData: { mimeType: "image/png", data: mask } });
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [{ parts }],
        generationConfig: {
          responseModalities: ["IMAGE"]
        }
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Gemini API Error:', errorData);
      return res.status(response.status).json({ error: 'Gemini API Error', details: errorData });
    }

    const data = await response.json();
    
    // 生成された画像データを探して返却
    const imageData = data.candidates?.[0]?.content?.parts?.find(p => p.inlineData)?.inlineData?.data;

    if (!imageData) {
      // 画像が返ってこなかった場合 (テキストのみの場合など)
      const textResponse = data.candidates?.[0]?.content?.parts?.[0]?.text;
      return res.status(200).json({ text: textResponse });
    }

    res.status(200).json({ image: imageData });
  } catch (error) {
    console.error('Server error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}
