# Runbook 04: IT support troubleshooting cases

## Case 1: Domain login or account lockout

Record the issue and approval, confirm the user is in the test domain, inspect AD user status (locked/disabled/expired), review domain controller logs, and test authentication after authorised intervention. Log ticket outcome and root cause. Do not publish real usernames, event logs or passwords.

## Case 2: Group Policy not applying

Check workstation OU placement, security filtering, inheritance, DNS and domain-controller reachability. Capture redacted `gpresult /r` and check Group Policy operational logs. Validate a single test GPO before making larger changes.

## Case 3: Entra join vs Intune enrollment

`dsregcmd /status` exposes device registration and join state, which is not equivalent to proof of active MDM policy enforcement. Look for Intune device inventory and last check-in, compliance and app-install evidence. Validate license and scope if missing.

## Case 4: Ticket nearing SLA

Determine the agreed priority, schedule, paused state and proper escalation rule. For this repo's demo use the fictional clock-hour targets only. Do not mistake a sample SLA calculation for actual osTicket timestamps or employer metrics.
