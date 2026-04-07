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
    
    // クライアントからの指定があればそれを使用し、なければ用途に応じてモデルを選択
    // gemini-2.0-flash-exp はマルチモーダルに強いが、純粋な翻訳などは 1.5-flash が安定
    const isMultimodal = !!(req.body.image || req.body.mask || (req.body.contents && JSON.stringify(req.body.contents).includes("inlineData")));
    // 確実に動作が確認されているモデル名に統一
    const requestedModel = req.body.model || "gemini-2.0-flash-exp"; 
    
    const model = genAI.getGenerativeModel({ model: requestedModel });

    let result;

    // A. 既存の Gemini 生リクエスト形式 (contents がある場合)
    if (req.body.contents) {
      result = await model.generateContent({
        contents: req.body.contents,
        generationConfig: req.body.generationConfig, // 呼び出し側の明示的な指定を優先
        safetySettings: req.body.safetySettings
      });
    } 
    // B. Imagen 互換形式 (instances パラメータなど)
    else if (req.body.instances) {
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

      const config = (image || mask) ? { responseModalities: ["IMAGE", "TEXT"] } : {};
      result = await model.generateContent({
        contents: [{ role: "user", parts }],
        generationConfig: config
      });
    }

    const response = await result.response;
    
    // 検証
    if (!response.candidates || response.candidates.length === 0) {
      throw new Error("AI returned no candidates. This may be due to safety filters.");
    }

    // 画像レスポンスの抽出 (inlineData)
    const partWithImage = response.candidates?.[0]?.content?.parts?.find(p => p.inlineData);
    if (partWithImage) {
      return res.status(200).json({ 
        image: partWithImage.inlineData.data,
        bytesBase64Encoded: partWithImage.inlineData.data,
        predictions: [{ bytesBase64Encoded: partWithImage.inlineData.data }],
        candidates: response.candidates 
      });
    }

    // 通常のテキストレスポンス
    const text = response.text ? response.text() : response.candidates[0].content.parts[0].text;
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
