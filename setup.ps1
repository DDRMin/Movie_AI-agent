# AI Agent Setup Script for Windows PowerShell

Write-Host "🤖 AI Agent Setup Script" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (!(Test-Path "ai_agent_env")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv ai_agent_env
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Install requirements
Write-Host "📚 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check if .env file exists
if (!(Test-Path ".env")) {
    Write-Host "⚙️ Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env file created" -ForegroundColor Green
    Write-Host "⚠️  IMPORTANT: Please edit .env file and add your GROQ_API_KEY" -ForegroundColor Red
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Create documents folder if it doesn't exist
if (!(Test-Path "documents")) {
    New-Item -ItemType Directory -Path "documents"
    Write-Host "✅ Documents folder created" -ForegroundColor Green
} else {
    Write-Host "✅ Documents folder already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file and add your GROQ_API_KEY from https://console.groq.com/keys" -ForegroundColor White
Write-Host "2. (Optional) Add MEM0_API_KEY from https://mem0.ai for persistent memory" -ForegroundColor White
Write-Host "3. Run: python agent_.py" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see SETUP.md" -ForegroundColor Gray
