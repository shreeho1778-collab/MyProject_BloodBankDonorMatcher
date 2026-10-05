# Requirements Traceability Matrix (RTM)

## Blood Bank Inventory & Emergency Donor Matcher

| Requirement ID | Requirement Type | Requirement Summary | Related Use Case | Verification / Test Method | Status |
|---|---|---|---|---|---|
| FR-001 | Functional | Cross-reference emergency blood requests with real-time inventory and notify compatible donors within 10 km. | Emergency Donor Matching & Notification | Functional Test | Planned |
| FR-002 | Functional | Temporarily hold a matched blood unit to prevent concurrent allocation. | Reserve Blood Unit | Functional Test | Planned |
| FR-003 | Functional | Verify donor eligibility before including a donor in matching results. | Verify Donor Eligibility | Functional Test | Planned |
| FR-004 | Functional | Track blood-component expiry, notify the manager 48 hours before expiry, and quarantine expired units. | Monitor Blood Inventory | Functional Test | Planned |
| FR-005 | Functional | Register and maintain searchable donor profiles. | Register Donor | Functional Test | Planned |
| NFR-001 | Non-Functional | Maintain transactional consistency and prevent simultaneous allocation of the same blood bag. | Reserve Blood Unit | Performance / Concurrency Test | Planned |
| NFR-002 | Non-Functional | Maintain 99.9% availability and fail over to a backup SMS gateway when required. | Emergency Donor Matching & Notification | Availability / Failover Test | Planned |
