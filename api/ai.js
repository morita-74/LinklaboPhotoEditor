/**
 * Vercel Serverless Function: Gemini API Proxy
 * APIキーをサーバーサイドで管理し、クライアントから隠蔽します。
 */

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { prompt, image } = req.body;
  const apiKey = process.env.GEMINI_API_KEY;

  if (!apiKey) {
    return res.status(500).json({ error: 'GEMINI_API_KEY is not set in environment variables.' });
  }

  try {
    // 最新モデル gemini-1.5-flash を使用 (画像生成/画像編集に対応しているバージョンを選択)
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [
          {
            parts: [
              { text: prompt },
              {
                inlineData: {
                  mimeType: "image/png",
                  data: image
                }
              }
            ]
          }
        ],
        generationConfig: {
          // 画像編集・生成を期待するための設定 (モデルが対応している場合に有効)
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
