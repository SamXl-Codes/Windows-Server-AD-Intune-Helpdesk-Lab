#Requires -Version 5.1
<# Read-only AD report. Run in an authorised and connected lab domain. #>
[CmdletBinding()]
param([string]$OutputDirectory = '.\evidence-local')
$ErrorActionPreference = 'Stop'
Import-Module ActiveDirectory -ErrorAction Stop
$domain = Get-ADDomain -ErrorAction Stop
if ($domain.DNSRoot -ne 'corp.lab.example') { throw 'Not the designated lab domain; refusing inventory export.' }
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$ous = @(Get-ADOrganizationalUnit -Filter * -SearchBase $domain.DistinguishedName |
    Select-Object Name,DistinguishedName)
$groups = @(Get-ADGroup -Filter * -SearchBase $domain.DistinguishedName |
    Where-Object { $_.Name -like 'SG-Lab-*' } | Select-Object Name,GroupScope)
$report = [pscustomobject]@{
    CapturedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    Domain = $domain.DNSRoot
    OrganisationalUnits = $ous
    LabGroups = $groups
    Note = 'Read-only lab inventory. Review for private names before publication.'
}
$report | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 (Join-Path $OutputDirectory 'ad-inventory.json')
Write-Host "Exported lab inventory to $OutputDirectory. Review for sensitive values before sharing."
