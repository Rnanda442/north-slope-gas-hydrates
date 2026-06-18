param(
    [switch]$GenerateLocalToken,
    [string]$BaseUrl = "",
    [string]$OutFile = "configs_local/private_sources.env"
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$outPath = Join-Path $projectRoot $OutFile
$outDir = Split-Path -Parent $outPath

if (-not (Test-Path -LiteralPath $outDir)) {
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
}

if ($GenerateLocalToken) {
    $bytes = New-Object byte[] 32
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try {
        $rng.GetBytes($bytes)
    } finally {
        $rng.Dispose()
    }
    $token = -join ($bytes | ForEach-Object { $_.ToString("x2") })
    $mode = "local_generated"
} else {
    $secure = Read-Host "Paste private source token" -AsSecureString
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        $token = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
    }
    $mode = "service_issued"
}

if ([string]::IsNullOrWhiteSpace($token)) {
    throw "Token cannot be empty."
}

$lines = @(
    "# Local only. This file is ignored by git.",
    "# Generated: $(Get-Date -Format o)",
    "HYDRATE_PRIVATE_SOURCE_MODE=$mode",
    "HYDRATE_PRIVATE_SOURCE_BASE_URL=$BaseUrl",
    "HYDRATE_PRIVATE_SOURCE_AUTH_SCHEME=Bearer",
    "HYDRATE_PRIVATE_SOURCE_TOKEN=$token"
)

Set-Content -LiteralPath $outPath -Value $lines -Encoding UTF8
Write-Host "Configured private source token at $outPath"
Write-Host "Secret value was not printed. Keep this file local."
