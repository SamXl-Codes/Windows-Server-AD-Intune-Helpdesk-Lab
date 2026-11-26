# Runbook 01: Windows Server 2022, AD DS and Group Policy

**Status:** Reference procedure. Its presence is not proof that the user performed these steps.

## Lab prerequisites

- Windows Server 2022 evaluation or properly licensed VM with a private host-only network, plus a separate Windows 11 VM.
- Isolated DNS, static IP plan and VM checkpoints; do not expose the domain controller to the internet.
- Local administrator access to the test server; adequate RAM/disk and backups.
- Use a **lab domain only**, such as `corp.lab.example`, not a company-owned live domain.

## Phase A: Configure AD DS

1. Record the VM build version from `winver` and `Get-ComputerInfo | Select WindowsProductName,OsVersion`.
2. Set a known static IP, and after promotion use the lab domain controller for DNS resolution.
3. Add the AD DS and DNS roles with Server Manager or `Install-WindowsFeature AD-Domain-Services -IncludeManagementTools`.
4. In Server Manager, promote as a new forest for `corp.lab.example` using the deployment wizard. **Record the DSRM password securely, never in this repo.**
5. Restart, verify `Get-ADDomain`, `Get-ADForest` and DNS resolution, and take a VM checkpoint.
6. Using ADUC, create `OU=LabUsers`, `OU=LabDevices`, `OU=LabGroups` and the `SG-Lab-*` security groups from the proposed design.
7. Run the provisioning PowerShell script **without** `-Apply` to preview, then use `-Apply -WhatIf` before a small confirmed test apply.

> These commands will alter the lab server and require domain admin rights. Perform them manually only after checking isolation and backups; the repository does not automatically promote a controller.

## Phase B: GPO testing

1. In Group Policy Management Console, create a **lab-only** workstation policy and link only to `OU=LabDevices`.
2. Test screen-lock timeout, Firewall baseline and user rights in a disconnected client VM; avoid disruptive domain-wide settings.
3. Add the Windows 11 device to the isolated domain and move its object into `OU=LabDevices`.
4. Run `gpupdate /force`, `gpresult /r` and inspect Event Viewer for `GroupPolicy/Operational` errors.
5. Export a test GPO report to a **local private path** with `Get-GPOReport -Name 'Lab Workstation Policy' -ReportType Html -Path .\evidence-local\gpo-report.html` if the policy exists.

## Phase C: Validation and rollback

Check DNS SRV records, test a lab account login, verify GPO scope, check that the account has only required group membership and test the account-lockout/reset runbook.

If a policy causes unwanted behaviour, unlink the test GPO from the test OU and run `gpupdate /force`; if the domain configuration fails, restore a validated VM checkpoint. Never delete a production domain as a rollback method.

## Evidence required to demonstrate completion

Actual redacted screenshots of Server Manager, ADUC OUs/groups, GPMC GPO link and RSoP plus a `Get-ADDomain` report; see the evidence checklist.
