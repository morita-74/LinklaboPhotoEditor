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
    pause
    exit /b
)

echo [1/3] 変更をスキャン中...
git add .

:: 変更があるかチェック
git status --short | findstr /R "^" > nul
if %errorlevel% neq 0 (
    echo [INFO] 変更はありません。送信（Push）ステップへ進みます。
    goto :push_step
)

echo [2/3] コミットを作成中...
:: コミット
git commit -m "Auto-update: %DATE% %TIME%"

:push_step
echo [3/3] GitHubへ送信中 (mainブランチ)...
:: プッシュを実行
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] デプロイに失敗しました。
    echo.
    echo 【確認点】
    echo ・一度「git pull origin main」を実行して競合を解消してください。
    echo ・ブラウザ等でGitHubへのログイン画面が出ていないか確認してください。
    echo ・コマンドプロンプトで直接「git push origin main」を叩いてエラーを確認してください。
    color 0C
) else (
    echo.
    echo [SUCCESS] GitHubへのアップロードが完了しました！
    color 0A
)

echo.
echo ========================================
pause
