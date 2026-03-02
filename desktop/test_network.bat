@echo off
setlocal enabledelayedexpansion

:: 定義要測試的國際目標 (Google, Cloudflare, OpenDNS 等)
set targets=google.com 8.8.8.8 1.1.1.1 208.67.222.222 github.com

echo [INFO] 正在啟動異步網絡測試...
echo --------------------------------------------------

:: 循環啟動併發進程
for %%i in (%targets%) do (
    :: 使用 start /b 在同一個窗口的後台執行，減少窗口彈出
    start /b cmd /c "ping -n 4 %%i | findstr /R /C:"[0-9]ms""
    echo [LAUNCH] 測試目標: %%i 已啟動...
)

echo --------------------------------------------------
echo [INFO] 測試完成後結果將自動顯示在下方。
echo [提示] 如果完全沒有回顯，可能存在嚴重的國際出口攔截。
pause
