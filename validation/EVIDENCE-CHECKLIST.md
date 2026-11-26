# Evidence checklist: replace demo visuals with verified, redacted captures

The README currently shows two conceptual SVG diagrams and two screenshots of the **synthetic ticket analyzer**. No genuine infrastructure or SaaS admin-console screenshots were available when the repository package was created.

A complete implementation evidence set should include:

| Area | Genuine evidence needed | Important redactions |
|---|---|---|
| Windows Server | `winver` / `Get-ComputerInfo`, AD DS Server Manager role and `Get-ADDomain` | Domain secrets, private hostnames/IPs |
| AD DS | ADUC OUs, lab groups, test users and a read-only user inventory | Real names, usernames, UPNs |
| Group Policy | GPMC GPO link and a redacted RSoP report from an affected client | Domain and network IDs |
| Entra / Intune | Actual join and MDM status; enrolled test device, compliance report and update ring result | Tenant IDs, device IDs, usernames, serials |
| Help Desk | osTicket queue, categorisation, documented resolution and configured SLA dashboard | Ticket text, customer names, email, IPs |

## Provenance metadata for any future real screenshot

For each file, add the date captured, lab environment, steps performed, application/version and a one-sentence explanation of exactly what the image demonstrates. Avoid claim inflation: **configured** is not the same as **deployed**, **assigned** is not the same as **applied**, and **synthetic sample** is not the same as **production incident**.

Only upload screenshots from your own authorised labs. Never scrape third-party dashboards and present them as your work.
