---
name: email-marketing/authentication
description: >
  Email authentication setup and troubleshooting (SPF, DKIM, DMARC) and the
  transactional vs marketing email distinction. Reference this when setting up
  sending infrastructure, diagnosing block bounces, or explaining authentication
  to a non-technical audience.
---

# Email Authentication

Authentication protects deliverability and domain reputation. Set this up before doing anything else.

## SPF (Sender Policy Framework)

**What it is:** A DNS TXT record listing IP addresses authorised to send email from your domain.

**How it works:** ISP's check incoming mail against your SPF record to verify the sending IP is authorised.

**Key implementation rules:**
- Only ONE SPF record is permitted per domain. If you have multiple sending services, merge them into a single record.
- Syntax errors silently break the whole record.
- Must include all services sending on your behalf: your ESP, transactional provider, CRM, etc.

**Qualifiers:**
- `~all` = soft fail (messages from unlisted IP's are marked suspicious but delivered)
- `-all` = hard fail (messages from unlisted IP's are rejected)
- `?all` = neutral (no policy)

**Example:** `v=spf1 include:_spf.google.com include:sendgrid.net ~all`

**Historical note:** Proposed 2003, widely adopted by major ISP's by mid-2000s.

## DKIM (DomainKeys Identified Mail)

**What it is:** A cryptographic signing mechanism that proves an email came from your domain and wasn't modified in transit.

**How it works:** Your mail server signs outgoing emails with a private key. The corresponding public key is published in your DNS. ISP's verify the signature using the public key.

**Key implementation rules:**
- Your ESP will generate the key pair and provide the DNS record to add.
- The DKIM selector in the email header must match the selector in your DNS record.
- If you rotate keys, update DNS promptly.

**Analogy:** A wax seal on a letter. Proves authenticity and tamper-evidence.

**Historical note:** Proposed 2004, standardised 2007.

## DMARC (Domain-based Message Authentication, Reporting & Conformance)

**What it is:** A policy layer that builds on SPF and DKIM. Tells receiving servers what to do with mail that fails authentication. Provides reporting back to you.

**Policies:**
- `p=none` — Monitor only. Emails pass regardless. Good starting point to gather data.
- `p=quarantine` — Failed emails go to spam folder.
- `p=reject` — Failed emails are blocked entirely.

**Why it matters:** Required by Gmail and Yahoo for bulk senders (as of 2024). Essential for brand protection against spoofing and phishing attacks using your domain.

**Recommended implementation order:** SPF → DKIM → DMARC (start with `p=none`, monitor reports, tighten policy over time)

## Troubleshooting Authentication

Common problems and their fixes:

| Problem | Symptom | Fix |
|---|---|---|
| Multiple SPF records | Block bounces, authentication failures | Merge into single record |
| Syntax error in SPF | All authentication fails silently | Validate with MXToolbox |
| DKIM selector mismatch | DKIM fails despite DNS record existing | Verify selector string matches in both header and DNS |
| DNS propagation | Records not taking effect immediately | Wait up to 48 hours, then recheck |
| ESP not included in SPF | Block bounces from ESP sends | Add ESP's SPF include to your record |

**Validation tools:** MXToolbox, mail-tester.com, Google Admin Toolbox (Check MX)

## Transactional vs Marketing Email

Understanding this distinction is important for legal compliance and infrastructure decisions.

| Dimension | Transactional | Marketing |
|---|---|---|
| Relationship type | 1-to-1 | 1-to-many |
| Initiator | Subscriber's action triggers it | Marketer initiates it |
| Content | Specific to the user's action | Promotional or informational |
| Opt-in required | No (within legal limits) | Yes |
| Typical examples | Order confirmations, password resets, double opt-in emails, shipping notifications | Newsletters, promotional campaigns, welcome sequences |
| Sending infrastructure | Often requires specialist platform or API integration | Standard ESP bulk sending |

**Welcome sequences are NOT transactional.** They're triggered by a subscription event, but they're marketing messages. Don't conflate them.

**Infrastructure note:** Transactional sends typically require a specialist provider (Mandrill, SparkPost, Postmark, SendGrid transactional) or direct API integration with your ESP. Many standard ESP bulk sending setups are not appropriate for transactional volume or deliverability requirements. Developer involvement is often necessary.
