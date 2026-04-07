import { GoogleGenerativeAI } from "@google/generative-ai";

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
    const genAI = new GoogleGenerativeAI(apiKey);
    
    // 基本的な画像編集/生成には gemini-1.5-flash を使用 (高速)
    // 画像生成 (Imagen等) が必要な場合は別のモデルを指定する必要がありますが、
    // 現状の Gemini API (v1) では generateContent で multimodal に対応。
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

    const parts = [
      { text: prompt }
    ];

    if (image) {
      parts.push({
        inlineData: {
          mimeType: "image/png",
          data: image
        }
      });
    }

    if (mask) {
      parts.push({ text: "Below is the mask image. The red colored areas indicate the regions to focus on or modify. Please fill them naturally based on the background context provided in the first image." });
      parts.push({
        inlineData: {
          mimeType: "image/png",
          data: mask
        }
      });
    }

    const result = await model.generateContent({
      contents: [{ role: "user", parts }],
      generationConfig: {
        // 画像編集結果として画像を返してほしい場合は、モデルに示唆する必要があります。
        // ※Gemini 1.5-flash自体が直接画像Binaryをレスポンスに含めるパターン(Imagen 3連携等)は
        // プレビュー段階や特定の権限が必要な場合がありますが、ここでは標準的なSDK実装を行います。
        responseModalities: ["IMAGE", "TEXT"] 
      }
    });

    const response = await result.response;
    const candidates = response.candidates;
    
    if (!candidates || candidates.length === 0) {
      return res.status(500).json({ error: 'No response from AI' });
    }

    // 生成された画像データを探す
    const partWithImage = response.candidates[0].content.parts.find(p => p.inlineData);
    
    if (partWithImage) {
      return res.status(200).json({ image: partWithImage.inlineData.data });
    }

    // 画像がない場合はテキストを返す
    const text = response.text();
    res.status(200).json({ text });

  } catch (error) {
    console.error('Server error:', error);
    res.status(500).json({ 
      error: 'Internal Server Error', 
      details: error.message 
    });
  }
}
