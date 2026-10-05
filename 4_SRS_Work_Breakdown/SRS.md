# Software Requirements Specification (SRS)

## Blood Bank Inventory & Emergency Donor Matcher

### 1. Introduction

#### 1.1 Purpose
The Blood Bank Inventory & Emergency Donor Matcher is a system designed to manage blood inventory and support emergency blood requests by identifying compatible and eligible donors.

#### 1.2 Scope
The system manages blood-unit inventory, donor profiles, emergency blood requests, donor eligibility, blood-unit reservations, expiry monitoring, and emergency donor notifications.

### 2. Stakeholders / Actors

- Emergency Requester
- Blood Bank Manager
- Donor
- SMS Gateway (External System)

### 3. Functional Requirements

#### FR-001 – Emergency Blood Matching and Notification
The system shall cross-reference emergency blood unit requests with real-time blood bank inventory and notify compatible donors within a 10 km radius.

#### FR-002 – Blood Unit Reservation
The system shall temporarily reserve a matched blood unit for a configurable period after an emergency request is confirmed, preventing concurrent allocation of the same unit.

#### FR-003 – Donor Eligibility Verification
The system shall verify donor eligibility, including the minimum 56-day gap since the last donation, age, and medical eligibility flags, before including a donor in matching results.

#### FR-004 – Blood Expiry Monitoring
The system shall track the expiry date of each blood component, notify the Blood Bank Manager 48 hours before expiry, and automatically quarantine expired units.

#### FR-005 – Donor Registration
The system shall allow the Blood Bank Manager to register donor profiles containing blood group, contact number, geographical location, and donation history.

### 4. Non-Functional Requirements

#### NFR-001 – Performance and Security
The inventory system shall maintain transactional consistency and prevent simultaneous allocation of the same physical blood unit.

#### NFR-002 – Availability and Reliability
The emergency matching and notification service shall maintain at least 99.9% uptime, excluding scheduled maintenance, and shall fail over to a backup SMS gateway if the primary gateway does not acknowledge dispatch within 5 seconds.

### 5. System Constraints

- The system requires accurate blood-group and donor information.
- Donor matching depends on donor eligibility information being available.
- Emergency notifications depend on SMS gateway availability.
- Blood inventory information must be kept up to date to prevent incorrect allocation.

### 6. Expected Outcome

The system should reduce emergency response time, prevent duplicate allocation of scarce blood units, avoid contacting ineligible donors, reduce wastage of expired blood components, and maintain reliable emergency notifications.
