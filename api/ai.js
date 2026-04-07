import { GoogleGenerativeAI } from "@google/generative-ai";

/**
 * Vercel Serverless Function: Gemini API Proxy
 * あらゆる既存のHTMLファイルからのリクエストをセキュアに仲介します。
 */
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'GEMINI_API_KEY is not set in environment variables.' });
  }

  try {
    const genAI = new GoogleGenerativeAI(apiKey);
    // 高速でマルチモーダルな gemini-1.5-flash を標準で使用
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

    let result;

    // A. 既存の Gemini 生リクエスト形式 (contents がある場合)
    if (req.body.contents) {
      result = await model.generateContent({
        contents: req.body.contents,
        generationConfig: req.body.generationConfig,
        safetySettings: req.body.safetySettings
      });
    } 
    // B. シンプルな { prompt, image } 形式
    else {
      const { prompt, image, mask } = req.body;
      const parts = [{ text: prompt }];

      if (image) {
        parts.push({
          inlineData: {
            mimeType: "image/png",
            data: image
          }
        });
      }

      if (mask) {
        parts.push({ text: "Below is the mask image for modification areas." });
        parts.push({
          inlineData: {
            mimeType: "image/png",
            data: mask
          }
        });
      }

      result = await model.generateContent({
        contents: [{ role: "user", parts }],
        generationConfig: {
            responseModalities: ["IMAGE", "TEXT"]
        }
      });
    }

    const response = await result.response;
    
    // 画像データが含まれているかチェック (inlineData)
    const partWithImage = response.candidates?.[0]?.content?.parts?.find(p => p.inlineData);
    if (partWithImage) {
      return res.status(200).json({ 
        image: partWithImage.inlineData.data,
        candidates: response.candidates // 元の互換性のために candidates も返す
      });
    }

    // 通常のテキストレスポンス
    const text = response.text();
    res.status(200).json({ 
      text, 
      candidates: response.candidates 
    });

  } catch (error) {
    console.error('Server error:', error);
    res.status(500).json({ 
      error: 'Internal Server Error', 
      details: error.message 
    });
  }
}
