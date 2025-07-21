# ============================================================================
# Environment Configuration Loader
# ============================================================================
# This script loads environment variables following the proper hierarchy:
# 1. Shared configuration (.env.shared)
# 2. Environment-specific configuration (.env.{environment})
# 3. Shared secrets (.env.secrets.shared) 
# 4. Environment-specific secrets (.env.secrets.{environment})

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("development", "staging", "production")]
    [string]$Environment,
    
    [switch]$Verbose = $false,
    [switch]$ValidateOnly = $false,
    [switch]$ShowSecrets = $false
)

# Script configuration
$ErrorActionPreference = "Stop"
$logFile = ".\environment_load_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

function Write-Log {
    param($Message, $Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "$timestamp [$Level] - $Message"
    
    # Output to console with color coding
    switch ($Level) {
        "ERROR" { Write-Host $logMessage -ForegroundColor Red }
        "WARNING" { Write-Host $logMessage -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $logMessage -ForegroundColor Green }
        default { Write-Host $logMessage -ForegroundColor White }
    }
    
    # Also log to file
    $logMessage | Out-File $logFile -Append
}

function Test-EnvironmentFile {
    param(
        [string]$FilePath,
        [string]$FileDescription
    )
    
    if (-not (Test-Path $FilePath)) {
        Write-Log "Missing required file: $FileDescription at $FilePath" "WARNING"
        return $false
    } else {
        Write-Log "Found: $FileDescription at $FilePath" "SUCCESS"
        return $true
    }
}

function Load-EnvironmentFile {
    param(
        [string]$FilePath,
        [string]$FileDescription,
        [bool]$IsSensitive = $false
    )
    
    if (-not (Test-Path $FilePath)) {
        Write-Log "Skipping missing file: $FileDescription" "WARNING"
        return 0
    }
    
    try {
        $content = Get-Content $FilePath -ErrorAction Stop
        $variableCount = 0
        
        foreach ($line in $content) {
            # Skip comments and empty lines
            if ($line -match '^\s*#' -or $line -match '^\s*$') {
                continue
            }
            
            # Parse environment variable (KEY=VALUE format)
            if ($line -match '^([^=]+)=(.*)$') {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                
                # Remove surrounding quotes if present
                if ($value -match '^".*"$' -or $value -match "^'.*'$") {
                    $value = $value.Substring(1, $value.Length - 2)
                }
                
                # Set environment variable
                [Environment]::SetEnvironmentVariable($key, $value, "Process")
                $variableCount++
                
                # Log variable loading (mask sensitive values)
                if ($IsSensitive -and -not $ShowSecrets -and $value -ne "") {
                    $maskedValue = if ($value.Length -gt 8) { "$($value.Substring(0,4))...$($value.Substring($value.Length-4))" } else { "***MASKED***" }
                    Write-Log "Loaded: $key = $maskedValue"
                } else {
                    Write-Log "Loaded: $key = $value"
                }
            }
        }
        
        Write-Log "Successfully loaded $variableCount variables from $FileDescription" "SUCCESS"
        return $variableCount
        
    } catch {
        Write-Log "Error loading $FileDescription`: $($_.Exception.Message)" "ERROR"
        return 0
    }
}

function Validate-EnvironmentVariables {
    param([string]$Environment)
    
    Write-Log "Validating environment variables for $Environment environment..." "INFO"
    
    # Define required variables by category
    $requiredVars = @{
        "Application" = @("APP_NAME", "APP_VERSION", "ENVIRONMENT")
        "Database" = @("POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB")
        "Redis" = @("REDIS_HOST", "REDIS_PORT", "REDIS_DB")
        "External APIs" = @("SPOTIFY_CLIENT_ID", "OPENAI_API_KEY", "GITHUB_TOKEN")
    }
    
    $validationErrors = @()
    $totalChecked = 0
    $totalMissing = 0
    
    foreach ($category in $requiredVars.Keys) {
        Write-Log "Checking $category variables..." "INFO"
        
        foreach ($var in $requiredVars[$category]) {
            $totalChecked++
            $value = [Environment]::GetEnvironmentVariable($var)
            
            if ([string]::IsNullOrWhiteSpace($value)) {
                $validationErrors += "Missing required variable: $var ($category)"
                $totalMissing++
                Write-Log "❌ Missing: $var" "ERROR"
            } else {
                if ($var -match "(KEY|SECRET|TOKEN|PASSWORD)" -and -not $ShowSecrets) {
                    $maskedValue = if ($value.Length -gt 8) { "$($value.Substring(0,4))...$($value.Substring($value.Length-4))" } else { "***SET***" }
                    Write-Log "✅ Present: $var = $maskedValue" "SUCCESS"
                } else {
                    Write-Log "✅ Present: $var = $value" "SUCCESS"
                }
            }
        }
    }
    
    # Summary
    Write-Log "`n=== VALIDATION SUMMARY ===" "INFO"
    Write-Log "Total variables checked: $totalChecked" "INFO"
    Write-Log "Missing variables: $totalMissing" $(if ($totalMissing -eq 0) { "SUCCESS" } else { "ERROR" })
    
    if ($validationErrors.Count -gt 0) {
        Write-Log "`nValidation Errors:" "ERROR"
        foreach ($error in $validationErrors) {
            Write-Log "  - $error" "ERROR"
        }
        return $false
    } else {
        Write-Log "All required environment variables are present!" "SUCCESS"
        return $true
    }
}

# Main execution
try {
    Write-Log "Starting environment configuration loading for: $Environment" "INFO"
    Write-Log "Working directory: $(Get-Location)" "INFO"
    
    # Define file paths following the established hierarchy
    $basePath = "infrastructure\environments"
    $sharedConfigPath = "$basePath\shared\config\.env.shared"
    $sharedSecretsPath = "$basePath\shared\secrets\.env.secrets.shared"
    $envConfigPath = "$basePath\$Environment\config\.env.$Environment"
    $envSecretsPath = "$basePath\$Environment\secrets\.env.secrets.$Environment"
    
    # File existence check
    Write-Log "Checking for required environment files..." "INFO"
    $allFilesExist = $true
    
    $allFilesExist = (Test-EnvironmentFile $sharedConfigPath "Shared Configuration") -and $allFilesExist
    $allFilesExist = (Test-EnvironmentFile $envConfigPath "$Environment Configuration") -and $allFilesExist
    
    # Secrets files are optional for validation-only mode
    if (-not $ValidateOnly) {
        Test-EnvironmentFile $sharedSecretsPath "Shared Secrets Template" | Out-Null
        Test-EnvironmentFile $envSecretsPath "$Environment Secrets" | Out-Null
    }
    
    if ($ValidateOnly) {
        Write-Log "Validation-only mode: Skipping actual environment loading" "INFO"
        if ($allFilesExist) {
            Write-Log "All required configuration files are present" "SUCCESS"
            exit 0
        } else {
            Write-Log "Some required configuration files are missing" "ERROR"
            exit 1
        }
    }
    
    # Load environment files in the correct hierarchy order
    Write-Log "Loading environment variables in hierarchy order..." "INFO"
    $totalVariables = 0
    
    # 1. Load shared configuration (base settings)
    $totalVariables += Load-EnvironmentFile $sharedConfigPath "Shared Configuration"
    
    # 2. Load environment-specific configuration (overrides shared)
    $totalVariables += Load-EnvironmentFile $envConfigPath "$Environment Configuration"
    
    # 3. Load shared secrets template (if needed for reference)
    # Note: This is typically just a template, actual secrets come from environment-specific files
    
    # 4. Load environment-specific secrets (contains actual secret values)
    $totalVariables += Load-EnvironmentFile $envSecretsPath "$Environment Secrets" $true
    
    Write-Log "`n=== LOADING SUMMARY ===" "INFO"
    Write-Log "Total environment variables loaded: $totalVariables" "SUCCESS"
    Write-Log "Environment: $Environment" "INFO"
    
    # Validate loaded environment
    if (-not (Validate-EnvironmentVariables $Environment)) {
        Write-Log "Environment validation failed! Some required variables are missing." "ERROR"
        exit 1
    }
    
    Write-Log "Environment loading completed successfully!" "SUCCESS"
    Write-Log "Log file: $logFile" "INFO"
    
    exit 0
    
} catch {
    Write-Log "Critical error during environment loading: $($_.Exception.Message)" "ERROR"
    Write-Log "Stack trace: $($_.ScriptStackTrace)" "ERROR"
    exit 1
}
