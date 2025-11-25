#!/bin/bash

# ============================================
# 1) RUN PYTEST
# ============================================
echo "Running pytest..."
pytest --alluredir=allure-results

# ============================================
# 2) GENERATE REPORT
# ============================================
echo "Generating Allure report..."
allure generate allure-results -o allure-report --clean

# ============================================
# 3) START ALLURE SERVER (WSL)
# ============================================
echo "Starting Allure server..."

# Start the server in background and capture port
SERVER_OUTPUT=$(allure open allure-report 2>&1 >/dev/null &)
sleep 1

# Find which port Allure is using
PORT=$(netstat -lnpt 2>/dev/null | grep "java" | grep "LISTEN" | awk '{print $4}' | sed 's/.*://')

if [[ -z "$PORT" ]]; then
    echo "❌ Could not detect Allure port."
    exit 1
fi

echo "Allure server running on port: $PORT"

# ============================================
# 4) AUTO-OPEN WINDOWS BROWSER
# ============================================
WIN_URL="http://localhost:$PORT"

echo "Opening browser on Windows..."
powershell.exe -Command "Start-Process '$WIN_URL'"

echo "✅ Allure opened successfully at: $WIN_URL"


