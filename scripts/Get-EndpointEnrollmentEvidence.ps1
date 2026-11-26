#Requires -Version 5.1
<# Read-only endpoint diagnostic capture. Redacts common identifiers, but manual review is still required. #>
[CmdletBinding()]
param([string]$OutputDirectory = '.\evidence-local')
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$raw = (& dsregcmd.exe /status 2>&1 | Out-String)
if ($LASTEXITCODE -ne 0) { Write-Warning "dsregcmd returned $LASTEXITCODE" }
$redacted = $raw -replace '(?im)^(\s*(?:TenantId|DeviceId|Thumbprint|KeyContainerId|TenantName|UserEmail|UserPrincipalName|MdmUrl|MdmTouUrl|MdmComplianceUrl|MdmTermsOfUseUrl)\s*:\s*).+$','$1[REDACTED]'
$redacted = $redacted -replace '(?im)([\w.+-]+@[\w.-]+\.[A-Z]{2,})','[REDACTED-EMAIL]'
$target = Join-Path $OutputDirectory 'dsregcmd-redacted.txt'
$redacted | Set-Content -LiteralPath $target -Encoding UTF8
$events = @()
try {
    $events = @(Get-WinEvent -LogName 'Microsoft-Windows-DeviceManagement-Enterprise-Diagnostics-Provider/Admin' -MaxEvents 20 -ErrorAction Stop |
        Select-Object TimeCreated, Id, LevelDisplayName)
} catch { Write-Warning 'MDM diagnostic log unavailable.' }
$events | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'mdm-event-summary.json') -Encoding UTF8
Write-Host 'Read-only device status captured. Review all outputs for sensitive data before publishing.'
