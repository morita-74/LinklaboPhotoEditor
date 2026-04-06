# Linklabo Photo Editor (AI Studio Migration & Vercel Deploy)

このプロジェクトは、AI機能を Google AI Studio (Gemini API) に移行し、Vercel で安全に公開するための構成になっています。

## セットアップ手順

1. **GitHub へのアップロード**:
   このディレクトリの全ファイルを GitHub リポジトリにプッシュしてください。

2. **Vercel でプロジェクト作成**:
   Vercel ダッシュボードから「Add New Project」で上記のリポジトリを選択します。

3. **環境変数の設定 (重要)**:
   Vercel のプロジェクト設定 -> Environment Variables から以下を追加してください。
   - **Key**: `GEMINI_API_KEY`
   - **Value**: あなたの Gemini API Key ([Google AI Studio](https://aistudio.google.com/app/apikey) で取得可能)

4. **デプロイ**:
   「Deploy」ボタンを押すと公開されます。

## 技術スタック
- **Frontend**: HTML / Tailwind CSS / Vanilla JS
- **Backend**: Node.js (Vercel Serverless Functions)
- **AI**: Gemini 1.5 Flash (via Google AI Studio)
