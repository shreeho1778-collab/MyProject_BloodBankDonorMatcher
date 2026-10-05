# Requirements Table

## Problem Statement #12 | Healthcare & Telemedicine
### Blood Bank Inventory & Emergency Donor Matcher

**Stakeholders / Actors:** Emergency Requester, Blood Bank Manager, Donor, SMS Gateway (external system)

## Functional Requirements

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| FR-001 | Functional | The system shall cross-reference emergency blood unit requests against real-time blood bank inventory and broadcast SMS alerts to compatible donors within a 10 km radius. | High | **Pass:** Compatible donors notified within 30 seconds of emergency flag. **Fail:** Incompatible blood group alerted. | Immediate notification of compatible donors during a shortage directly reduces response time in a life-threatening situation. |
| FR-002 | Functional | The system shall place a temporary hold ("Reserved" status) on a matched blood unit for a configurable window (e.g. 30 minutes) once an emergency request is confirmed, preventing that unit from being allocated to a concurrent request. | High | **Pass:** Reserved unit's status changes to "Held" and is excluded from other search results until the hold expires or is confirmed. **Fail:** The same unit is shown as available to a second requester while a hold is active. | Prevents double-booking of scarce blood units during high-demand shortage events. |
| FR-003 | Functional | The system shall automatically verify a donor's eligibility (minimum 56-day gap since last donation, age, medical flags) before including them in a compatible-donor search result. | High | **Pass:** Ineligible donors are excluded from the notification list. **Fail:** A donor who donated 20 days ago is notified. | Protects donor health and avoids wasted outreach to donors who cannot legally/medically donate. |
| FR-004 | Functional | The system shall continuously track the expiry date of each blood component batch, send an alert to the Blood Bank Manager 48 hours before expiry, and auto-quarantine the unit once expired. | Medium | **Pass:** Manager receives an alert exactly 48 hours before expiry and expired units are auto-flagged "Do Not Use". **Fail:** An expired unit remains marked "Available". | Reduces wastage of perishable blood components and prevents accidental use of expired stock. |
| FR-005 | Functional | The system shall allow a Blood Bank Manager to register a new donor profile (blood group, contact number, geo-location, donation history), which becomes part of the searchable donor pool; donors may also self-register. | Medium | **Pass:** A newly registered donor with valid blood-group data appears in future compatible-donor searches. **Fail:** A registered donor with a missing blood-group field is included in search results. | A complete, validated donor pool is the foundation the entire emergency-matching feature depends on. |

## Non-Functional Requirements

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| NFR-001 | Performance & Security | The inventory ledger must maintain strict transactional consistency, preventing simultaneous allocation of the same blood bag. | High | **Pass:** Benchmarking tests confirm target latency and security standards under simulated peak load. | Without atomic locking, two simultaneous emergency requests could allocate the same physical unit, causing a life-threatening shortfall at the point of transfusion. |
| NFR-002 | Availability & Reliability | The core emergency-matching and notification service shall maintain at least 99.9% uptime (excluding scheduled maintenance) and automatically fail over to a backup SMS gateway if the primary does not acknowledge dispatch within 5 seconds. | High | **Pass:** Failover to the backup gateway completes and the alert is delivered within 35 seconds total even when the primary gateway is down. **Fail:** System has no path to deliver alerts when the primary SMS gateway is unreachable. | Because the system is invoked during medical emergencies, downtime directly translates to delayed treatment or loss of life, making high availability non-negotiable. |
