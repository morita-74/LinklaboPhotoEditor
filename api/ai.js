import { GoogleGenerativeAI } from "@google/generative-ai";

/**
 * Vercel Serverless Function: Universal Gemini/Imagen API Proxy
 * あらゆる既存のHTMLファイル（20種類以上）からのリクエストをセキュアに仲介します。
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
    
    // クライアントからの指定があればそれを使用し、なければ汎用的なモデルを使用
    const requestedModel = req.body.model || "gemini-2.0-flash-exp"; 
    
    // Imagen などの「predict」系リクエストの暫定対応（必要に応じてモデルを切り替え）
    // 実際にはImagen 3/4もgenerateContentで抽象化できるモデルが増えていますが、
    // ここでは20以上のツールの多様な用途に応えるため、常に最新のマルチモーダルモデルを使用します。
    const model = genAI.getGenerativeModel({ model: requestedModel });

    let result;

    // A. 既存の Gemini 生リクエスト形式 (contents がある場合)
    if (req.body.contents) {
      result = await model.generateContent({
        contents: req.body.contents,
        generationConfig: req.body.generationConfig || { responseModalities: ["TEXT", "IMAGE"] },
        safetySettings: req.body.safetySettings
      });
    } 
    // B. Imagen 互換形式 (instances パラメータなど)
    else if (req.body.instances) {
        // Imagen リクエストを Gemini 2.0 にマッピング（画像生成能力を持つモデルに転送）
        const prompt = req.body.instances.prompt || req.body.instances[0].prompt;
        result = await model.generateContent({
            contents: [{ role: "user", parts: [{ text: prompt }] }],
            generationConfig: { responseModalities: ["IMAGE"] }
        });
    }
    // C. シンプルな { prompt, image } 形式
    else {
      const { prompt, image, mask } = req.body;
      const parts = [{ text: prompt || "何か描いてください" }];

      if (image) {
        parts.push({
          inlineData: {
            mimeType: "image/png",
            data: image.includes(",") ? image.split(",")[1] : image
          }
        });
      }

      if (mask) {
        parts.push({ text: "Below is the mask image for modification areas. Please fill the mask area based on the surroundings." });
        parts.push({
          inlineData: {
            mimeType: "image/png",
            data: mask.includes(",") ? mask.split(",")[1] : mask
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
    
    // 画像レスポンスの抽出 (inlineData)
    const partWithImage = response.candidates?.[0]?.content?.parts?.find(p => p.inlineData);
    if (partWithImage) {
      // 既存ツールとの互換性のため、複数の形式で画像データを返す
      return res.status(200).json({ 
        image: partWithImage.inlineData.data,
        bytesBase64Encoded: partWithImage.inlineData.data, // Imagen互換
        predictions: [{ bytesBase64Encoded: partWithImage.inlineData.data }], // Predict互換
        candidates: response.candidates 
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
