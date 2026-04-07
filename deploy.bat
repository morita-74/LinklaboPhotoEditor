@echo off
setlocal
:: 文字コードをUTF-8に設定
chcp 65001 > nul

:: バッチファイルがある場所をカレントディレクトリにする
cd /d "%~dp0"

echo ========================================
echo Linklabo Project - GitHub Deployment
echo ========================================
echo.

:: Gitリポジトリかチェック
if not exist ".git" (
    echo [ERROR] このフォルダはGitリポジトリではありません。
    echo git init を実行するか、正しいフォルダにバッチを置いてください。
    pause
    exit /b
)

echo [1/3] 変更をスキャン中...
git add .

:: 変更があるかチェック
git status --short | findstr /R "^" > nul
if %errorlevel% neq 0 (
    echo [INFO] 変更はありません。送信をスキップします。
    goto :push_step
)

echo [2/3] コミットを作成中...
:: コミットメッセージにスペースを含めるため引用符で囲む
git commit -m "Auto-update: %DATE% %TIME%"

:push_step
echo [3/3] GitHubへ送信中 (mainブランチ)...
:: --force を使わず、安全にプッシュ（必要に応じて git pull を促すメッセージが出るようにする）
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] デプロイに失敗しました。
    echo 原因の可能性:
    echo 1. ネットワーク環境の問題
    echo 2. GitHubの認証エラー (ログインが必要かもしれません)
    echo 3. リモート側に新しい変更がある (git pull が必要)
    echo.
    echo 詳細を確認するには、コマンドプロンプトで直接 "git push origin main" を実行してください。
    color 0C
) else (
    echo.
    echo [SUCCESS] GitHubへのアップロードが完了しました！
    color 0A
)

echo.
echo ========================================
pause
