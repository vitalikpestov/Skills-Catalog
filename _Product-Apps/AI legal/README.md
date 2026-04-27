<p align="center">
  <img src="assets/banner.svg" alt="AI Legal Assistant for Claude Code" width="900"/>
</p>

<p align="center">
  <strong>AI-powered contract review and legal document generation.</strong> Review contracts, flag risks,<br/>
  generate NDAs, check compliance, negotiate terms, and produce client-ready PDF reports — all from Claude Code.
</p>

<p align="center">
  Every contract has hidden risks. This tool finds them in 60 seconds.
</p>

---

## Why This Matters

| Metric | Value |
|--------|-------|
| Average legal review cost | $300–$500/hour |
| Basic contract review | $1,500–$3,000 |
| Freelancers who don't read contracts | 82% |
| Cost of one bad clause | $10,000+ |
| Small businesses without legal review | 67% |
| Time to review with this tool | Under 60 seconds |

---

## Quick Start

```bash
curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-legal-claude/main/install.sh | bash
```

That's it. One command installs all 14 skills, 5 agents, and the PDF generation scripts.

---

## All 14 Commands

### Contract Analysis
| Command | What It Does |
|---------|-------------|
| `/legal review <file>` | **Flagship** — Full contract review with 5 parallel agents. Returns a Contract Safety Score, clause-by-clause analysis, and prioritized recommendations. |
| `/legal risks <file>` | Deep risk analysis with severity scoring for every clause. Estimates financial exposure. |
| `/legal compare <file1> <file2>` | Side-by-side comparison of two contract versions. Flags additions, removals, and dangerous changes. |
| `/legal plain <file>` | Translates every clause from legalese into plain English anyone can understand. |
| `/legal negotiate <file>` | Generates specific counter-proposals with replacement language for every unfavorable clause. |
| `/legal missing <file>` | Finds protections that SHOULD be in the contract but aren't. |

### Document Generation
| Command | What It Does |
|---------|-------------|
| `/legal nda <description>` | Generates a custom NDA — mutual, one-way, employee, or vendor. |
| `/legal terms <url>` | Generates terms of service based on what the website actually does. GDPR/CCPA compliant. |
| `/legal privacy <url>` | Generates a privacy policy by scanning what data the site collects. |
| `/legal agreement <type>` | Generates business agreements — freelancer contracts, partnerships, SOWs, MSAs, and more. |
| `/legal freelancer <file>` | Specialized review from the freelancer's perspective. Flags common contractor traps. |

### Compliance & Reporting
| Command | What It Does |
|---------|-------------|
| `/legal compliance <url>` | Compliance gap analysis — GDPR, CCPA, ADA, PCI-DSS, CAN-SPAM, SOC 2. |
| `/legal report-pdf` | Professional PDF report with score gauges, risk charts, and prioritized actions. |

---

## The Flagship: `/legal review`

The most powerful command. Run it on any contract and get:

1. **Contract Safety Score** (0-100) with letter grade
2. **Risk Dashboard** — high/medium/low risk clause counts
3. **Clause-by-Clause Analysis** — every clause scored, explained in plain English, with specific fix recommendations
4. **Missing Protections** — what should be there but isn't
5. **Obligations Timeline** — every deadline and consequence mapped
6. **Compliance Flags** — regulatory issues flagged
7. **Negotiation Priorities** — ranked list of what to change first
8. **Next Steps** — actionable checklist

### How It Works

```
/legal review my-contract.pdf
```

5 AI agents launch in parallel:

| Agent | Role | Weight |
|-------|------|--------|
| Clause Analyst | Identifies and categorizes every clause | 20% |
| Risk Assessor | Scores each clause for risk | 25% |
| Compliance Checker | Flags regulatory issues | 20% |
| Terms Mapper | Maps obligations, deadlines, and triggers | 15% |
| Recommendations Engine | Generates specific fixes | 20% |

Results are aggregated into a unified report with a single Contract Safety Score.

---

## Use Cases

### For Freelancers & Agencies
- Review client contracts before signing
- Generate NDAs for new client engagements
- Create statements of work with proper protections
- Offer contract review as a paid service ($500-$1,500 per review)

### For Small Businesses
- Review vendor and supplier contracts
- Generate privacy policies and terms of service
- Run compliance audits on your website
- Understand what you're actually agreeing to

### For AI Automation Agencies
- Add contract review to your service offering
- Generate professional PDF reports for clients
- Offer monthly legal document management retainers
- Pair with the AI Marketing Suite and AI Sales Team

---

## Project Structure

```
ai-legal-claude/
├── legal/
│   └── SKILL.md                    # Main orchestrator (command router)
├── skills/
│   ├── legal-review/SKILL.md       # Full contract review (5 agents)
│   ├── legal-risks/SKILL.md        # Deep risk analysis
│   ├── legal-compare/SKILL.md      # Contract comparison
│   ├── legal-plain/SKILL.md        # Plain English translation
│   ├── legal-negotiate/SKILL.md    # Counter-proposal generator
│   ├── legal-missing/SKILL.md      # Missing protections finder
│   ├── legal-nda/SKILL.md          # NDA generator
│   ├── legal-terms/SKILL.md        # Terms of service generator
│   ├── legal-privacy/SKILL.md      # Privacy policy generator
│   ├── legal-agreement/SKILL.md    # Business agreement generator
│   ├── legal-compliance/SKILL.md   # Compliance gap analysis
│   ├── legal-freelancer/SKILL.md   # Freelancer contract review
│   └── legal-report-pdf/SKILL.md   # PDF report generator
├── agents/
│   ├── legal-clauses.md            # Clause analysis agent
│   ├── legal-risks.md              # Risk assessment agent
│   ├── legal-compliance.md         # Compliance check agent
│   ├── legal-terms.md              # Terms & obligations agent
│   └── legal-recommendations.md    # Recommendations agent
├── scripts/
│   └── generate_legal_pdf.py       # PDF generation (ReportLab)
├── templates/
│   └── contract-review-template.md # Report template
├── install.sh                      # One-line installer
├── uninstall.sh                    # Clean uninstaller
└── README.md
```

---

## Requirements

- **Claude Code** (with an active Anthropic API key)
- **Python 3.8+** (for PDF generation only)
- **reportlab** — `pip3 install reportlab` (for PDF generation only)

---

## Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-legal-claude/main/uninstall.sh | bash
```

Or run locally:

```bash
./uninstall.sh
```

---

## Disclaimer

This tool is for educational and informational purposes only. It does **not** provide legal advice and should **not** be used as a substitute for consultation with a licensed attorney. Always have a qualified lawyer review any contract before signing.

---

<p align="center">
  <strong>Part of the Claude Code Skills Series</strong><br>
  <a href="https://github.com/zubair-trabzada/ai-marketing-claude">AI Marketing Suite</a> ·
  <a href="https://github.com/zubair-trabzada/ai-sales-team-claude">AI Sales Team</a> ·
  <strong>AI Legal Assistant</strong>
</p>

<p align="center">
  <a href="https://www.skool.com/aiworkshop">🎓 Learn How to Sell Claude Code Services to Real Businesses</a>
</p>
