# Runbook 02: Microsoft Entra ID, Intune, MFA and Windows update rings

**Status:** Documented procedure, not a record of a connected or configured tenant.

## Prerequisites

A licensed and authorised Microsoft Entra / Intune **test tenant**, a Windows 11 test device, test user licensing, appropriate administrator role and an allowed MDM enrollment scenario. Licensing/feature requirements change; review the linked Microsoft Learn documentation. Do not enroll unmanaged personal or company devices without authorisation.

## Exercises

1. Confirm the tenant's MDM authority and Windows enrollment settings; determine whether the test device is **Entra joined**, **hybrid joined**, or only **registered**. These are different states and should not be conflated.
2. Enroll a disposable Windows 11 test device through an allowed enrollment method. Check `dsregcmd /status` for domain/Entra join state (this is *not*, by itself, sufficient evidence of Intune management).
3. Confirm the device appears under Intune's Windows devices with a real last-check-in timestamp.
4. Create a lab-only compliance policy, assign it to the test device group, then review the device compliance results.
5. Create a lab Windows update ring (test group only), assign and verify reporting. Do not assume that policy assignment implies the update installed.
6. Assign a small test application and verify its **actual install status**, not merely assignment.
7. Configure MFA for authorised test users using the current supported Entra authentication/Conditional Access controls; do not confuse MFA with Intune compliance.
8. Troubleshoot enrollment via `dsregcmd /status`, `Event Viewer > Microsoft-Windows-DeviceManagement-Enterprise-Diagnostics-Provider/Admin` and current Intune reports.

## Validation and evidence

Collect actual, time-stamped, redacted screenshots of device management status, compliance evaluation, app install status and update-ring reporting. A screenshot of a wizard or configured policy without an assignment/real check-in is **not** evidence that it reached a device.

## Key references

- https://learn.microsoft.com/en-us/intune/device-enrollment/windows/guide
- https://learn.microsoft.com/en-us/entra/identity/devices/troubleshoot-device-dsregcmd
- https://learn.microsoft.com/en-us/intune/device-updates/windows/manage-update-rings
- https://learn.microsoft.com/en-us/troubleshoot/mem/intune/device-enrollment/troubleshoot-windows-auto-enrollment
