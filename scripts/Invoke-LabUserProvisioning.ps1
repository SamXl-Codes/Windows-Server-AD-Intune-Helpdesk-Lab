#Requires -Version 5.1
<#
.SYNOPSIS
  Safe-by-default provisioning plan for a dedicated test domain.
.DESCRIPTION
  Without -Apply, validates input and prints a preview; no AD module is loaded.
  With -Apply, checks current domain and targets only OU=LabUsers in corp.lab.example.
  New accounts are disabled, with no password set. This avoids storing credentials.
  Run only on an authorised isolated lab domain controller/admin workstation.
.EXAMPLE
  .\Invoke-LabUserProvisioning.ps1 -CsvPath .\configs\sample-users.csv
.EXAMPLE
  .\Invoke-LabUserProvisioning.ps1 -CsvPath .\configs\sample-users.csv -Apply -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [Parameter(Mandatory = $true)][string]$CsvPath,
    [switch]$Apply
)
$ErrorActionPreference = 'Stop'
$ExpectedDomain = 'corp.lab.example'
$records = @(Import-Csv -LiteralPath $CsvPath)
if ($records.Count -eq 0) { throw 'CSV contains no users.' }
$seen = @{}
foreach ($user in $records) {
    foreach ($field in @('GivenName','Surname','SamAccountName','Department','Title')) {
        if (-not ($user.PSObject.Properties.Name -contains $field)) { throw "Missing column: $field" }
        if ([string]::IsNullOrWhiteSpace($user.$field)) { throw "Empty $field for a user" }
    }
    $sam = $user.SamAccountName
    if ($sam -cnotmatch '^[a-z][a-z0-9._-]{2,19}$') { throw "Invalid sample account name: $sam" }
    if ($seen.ContainsKey($sam)) { throw "Duplicate account name: $sam" }
    $seen[$sam] = $true
}

if (-not $Apply) {
    Write-Host "PREVIEW ONLY: $($records.Count) disabled test accounts would be created in OU=LabUsers,$ExpectedDomain"
    $records | Select-Object GivenName,Surname,SamAccountName,Department,Title | Format-Table -AutoSize
    Write-Host 'No directory changes were attempted. Supply -Apply only after lab validation.'
    return
}

Import-Module ActiveDirectory -ErrorAction Stop
$domain = Get-ADDomain -ErrorAction Stop
if ($domain.DNSRoot -ne $ExpectedDomain) {
    throw "Refusing writes: expected $ExpectedDomain but connected to $($domain.DNSRoot)"
}
$targetOu = "OU=LabUsers,$($domain.DistinguishedName)"
Get-ADOrganizationalUnit -Identity $targetOu -ErrorAction Stop | Out-Null
foreach ($user in $records) {
    if (Get-ADUser -Filter "SamAccountName -eq '$($user.SamAccountName)'" -ErrorAction Stop) {
        Write-Warning "Skipping existing account: $($user.SamAccountName)"
        continue
    }
    $display = "$($user.GivenName) $($user.Surname)"
    if ($PSCmdlet.ShouldProcess("$display ($($user.SamAccountName)) in $targetOu", 'Create disabled test AD account')) {
        New-ADUser -Name $display -GivenName $user.GivenName -Surname $user.Surname `
            -SamAccountName $user.SamAccountName -Department $user.Department -Title $user.Title `
            -Path $targetOu -Enabled $false -ErrorAction Stop
        Write-Host "Created disabled lab account: $($user.SamAccountName)"
    }
}
