# Runbook 03: osTicket help desk workflows and example SLAs

**Status:** The repository includes an offline CSV simulator, not a deployed or connected osTicket server.

## Installation and safety

Install a supported osTicket release only in a private lab VM / container environment after reviewing the official requirements, HTTPS setup, database security and update guidance. Avoid unmaintained unofficial container images and publicly exposed test deployments. Do not include credentials or real tickets in Git.

## Suggested practice scenarios

- Password lockout: verify caller identity via approved procedure, check AD lockout status and document the resolution without exposing the reset secret.
- Joiner request: verify approvals, ticket classification and access entitlements before creating a disabled test account.
- Leaver request: verify identity and deprovisioning approvals; document controlled access removal and asset recovery.
- Noncompliant endpoint: determine whether the device is actually enrolled and check Intune's latest policy evaluation, not simply the policy assignment.
- Laptop connectivity: record DNS, IP, VPN and hardware/driver diagnostics before escalation.

## Example service-level objectives (fictional training targets)

| Priority | Sample elapsed clock-hour resolution target |
|---|---:|
| P1 | 4 |
| P2 | 8 |
| P3 | 24 |
| P4 | 72 |

**These are entirely illustrative, not osTicket defaults or any employer's contractual SLAs.** The offline Python reporter uses these example values and intentionally does not count business-hours, pausing, holidays or requester permissions. Configure the real lab's service calendar according to its own SLA rules.

## Working with tickets

Because the public osTicket developer API documentation lists ticket **creation** rather than general ticket retrieval, this project does **not** claim to pull incidents from osTicket's API. The included `sample-data/tickets.csv` is entirely fictional and demonstrates offline reporting. If you later export tickets through an appropriately authorised supported method, scrub personal and security-sensitive data before using them for demonstrations.

- https://docs.osticket.com/en/latest/Developer%20Documentation/API/Tickets.html
- https://docs.osticket.com/en/latest/
