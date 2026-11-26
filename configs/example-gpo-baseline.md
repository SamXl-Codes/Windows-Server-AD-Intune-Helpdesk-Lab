# Example GPO baseline (proposed configuration)

**Not a GPO backup or proof of application.** These are recommended exercises for an isolated domain test VM.

| Policy area | Example exercise | Evidence to collect |
|---|---|---|
| Account policy | Inspect password length/lockout settings in domain policy; choose test values only in lab | Screenshot of GPMC settings; `net accounts /domain` output with names removed |
| Workstations | Create a GPO for lab-only workstations; review security options and Windows Defender Firewall profile | GPO link screenshot and redacted RSoP report |
| Local permissions | Validate least-privilege group membership and delegated OU rights | Group membership export without personal details |
| Drive mapping (optional) | Test preference-driven mapping in an isolated OU | `gpresult /r` before/after and user-side test |

**Safety:** Do not apply arbitrary security baselines to existing domains. Work only in an isolated test domain, and test rollback and recovery before experimenting.
