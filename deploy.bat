@echo off
echo GitHubへアップロードを開始します...
git add .
git commit -m "Auto-update: %date% %time%"
git push origin main
echo.
echo ========================================
echo アップロードが完了しました！
echo Vercelでの更新が始まります（約1分で反映されます）。
echo ========================================
pause
