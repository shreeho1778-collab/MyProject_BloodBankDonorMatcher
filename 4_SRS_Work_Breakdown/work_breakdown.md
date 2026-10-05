# Work Breakdown Structure

## Blood Bank Inventory & Emergency Donor Matcher

| WBS ID | Task | Related Requirement |
|---|---|---|
| 1.0 | Requirements Engineering | All FRs and NFRs |
| 1.1 | Identify stakeholders and actors | — |
| 1.2 | Define functional requirements | FR-001 to FR-005 |
| 1.3 | Define non-functional requirements | NFR-001 to NFR-002 |
| 2.0 | System Architecture | FRs and NFRs |
| 2.1 | Design system components | FR-001 to FR-005 |
| 2.2 | Design database and data flow | FR-001, FR-002, FR-005 |
| 2.3 | Design notification and SMS failover | NFR-002 |
| 3.0 | Emergency Matching | FR-001, FR-003 |
| 3.1 | Process emergency blood request | FR-001 |
| 3.2 | Match blood units and donors | FR-001 |
| 3.3 | Verify donor eligibility | FR-003 |
| 3.4 | Send emergency notifications | FR-001 |
| 4.0 | Inventory Management | FR-002, FR-004 |
| 4.1 | Register and manage blood units | FR-004 |
| 4.2 | Reserve matched blood units | FR-002 |
| 4.3 | Monitor blood expiry | FR-004 |
| 5.0 | Donor Management | FR-003, FR-005 |
| 5.1 | Register donor profiles | FR-005 |
| 5.2 | Maintain donor information | FR-005 |
| 6.0 | Testing | All FRs and NFRs |
| 6.1 | Functional testing | FR-001 to FR-005 |
| 6.2 | Concurrency and consistency testing | NFR-001 |
| 6.3 | Availability and failover testing | NFR-002 |
