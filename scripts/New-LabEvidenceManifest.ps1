#Requires -Version 5.1
<#
.SYNOPSIS
  Generate a local SHA-256 inventory of REDACTED screenshots and reports.
.DESCRIPTION
  Read-only, offline script. Does not take screenshots, redact images, connect to
  tenants or upload anything. A hash documents file integrity, NOT authenticity.
.EXAMPLE
  .\scripts\New-LabEvidenceManifest.ps1 -CaptureDirectory .\evidence-local\captures
#>
[CmdletBinding()]
param(
    [string]$CaptureDirectory = '.\evidence-local\captures',
    [string]$OutputPath = '.\evidence-local\manifest-private.json'
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $CaptureDirectory -PathType Container)) {
    throw "Capture directory not found. Create it and add your own redacted images first: $CaptureDirectory"
}
$root = (Resolve-Path -LiteralPath $CaptureDirectory).Path.TrimEnd([char]'\', [char]'/')
$allowedExtensions = @('.png', '.jpg', '.jpeg', '.pdf', '.html', '.xml', '.txt')
$files = @(Get-ChildItem -LiteralPath $root -File -Recurse |
    Where-Object { $allowedExtensions -contains $_.Extension.ToLowerInvariant() } |
    Sort-Object FullName)
if ($files.Count -eq 0) { throw 'No evidence files found in the capture directory.' }
$items = @(
    foreach ($file in $files) {
        $relative = $file.FullName.Substring($root.Length).TrimStart([char]'\', [char]'/') -replace '\\', '/'
        [pscustomobject]@{
            RelativePath = $relative
            Sha256 = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            SizeBytes = $file.Length
            LastModifiedUtc = $file.LastWriteTimeUtc.ToString('o')
            CapturedAtUtc = $null
            LabEnvironment = $null
            ClaimSupported = $null
            RedactionReviewed = $false
            Note = 'Fill metadata, inspect file manually, and verify no identifiers or secrets before public upload.'
        }
    }
)
$manifest = [pscustomobject]@{
    GeneratedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    Disclaimer = 'Inventory and hashes only. Not evidence of independent validation or successful deployment.'
    Files = $items
}
$parentDir = Split-Path -Parent $OutputPath
if ($parentDir -and -not (Test-Path -LiteralPath $parentDir -PathType Container)) {
    New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
}
$manifest | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
Write-Output "Inventory written locally: $OutputPath"
Write-Output "Files indexed: $($files.Count). Nothing was uploaded or redacted."
