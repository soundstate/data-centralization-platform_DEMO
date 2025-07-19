# Test LLM Backend API Endpoints
Write-Host "Testing LLM Backend API..." -ForegroundColor Green

# Test Health Check
Write-Host "`n1. Testing Health Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:3001/health" -Method GET
    Write-Host "✓ Health Check: $($health.status) - $($health.message)" -ForegroundColor Green
} catch {
    Write-Host "✗ Health Check Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test Models Endpoint
Write-Host "`n2. Testing Models Endpoint..." -ForegroundColor Yellow
try {
    $models = Invoke-RestMethod -Uri "http://localhost:3001/api/models" -Method GET
    Write-Host "✓ Models Available:" -ForegroundColor Green
    foreach ($model in $models.available_models) {
        Write-Host "  - $($model.name): $($model.description)" -ForegroundColor Cyan
    }
} catch {
    Write-Host "✗ Models Endpoint Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test Chat Endpoint (simple test)
Write-Host "`n3. Testing Chat Endpoint..." -ForegroundColor Yellow
try {
    $body = @{
        message = "Hello"
    } | ConvertTo-Json

    $headers = @{
        "Content-Type" = "application/json"
    }

    Write-Host "Sending test message to LLM..." -ForegroundColor Cyan
    $chat = Invoke-RestMethod -Uri "http://localhost:3001/api/chat" -Method POST -Body $body -Headers $headers
    Write-Host "✓ Chat Response: $($chat.response)" -ForegroundColor Green
    Write-Host "  Model: $($chat.model)" -ForegroundColor Cyan
    Write-Host "  Timestamp: $($chat.timestamp)" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Chat Endpoint Failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode
        Write-Host "  Status Code: $statusCode" -ForegroundColor Red
    }
}

Write-Host "`nBackend API testing complete!" -ForegroundColor Green
Write-Host "You can now start the frontend by running 'npm start' in the ui/llm-frontend directory" -ForegroundColor Yellow
