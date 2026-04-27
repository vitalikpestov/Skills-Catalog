#!/usr/bin/env python3
"""Generate a realistic but intentionally flawed freelancer services agreement PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
import os

OUTPUT_PATH = "/Users/zubair/Documents/Claude Code/ai-legal-claude/sample-contract.pdf"

def build_contract():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        leftMargin=1*inch,
        rightMargin=1*inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'ContractTitle', parent=styles['Title'],
        fontSize=16, spaceAfter=6, alignment=TA_CENTER,
        fontName='Helvetica-Bold',
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=10, alignment=TA_CENTER, textColor=colors.grey,
        spaceAfter=20,
    )
    heading_style = ParagraphStyle(
        'SectionHead', parent=styles['Heading2'],
        fontSize=11, fontName='Helvetica-Bold',
        spaceBefore=14, spaceAfter=6,
    )
    body_style = ParagraphStyle(
        'ContractBody', parent=styles['Normal'],
        fontSize=9.5, leading=13, alignment=TA_JUSTIFY,
        fontName='Times-Roman', spaceAfter=4,
    )
    indent_style = ParagraphStyle(
        'Indented', parent=body_style,
        leftIndent=24, spaceAfter=4,
    )
    sub_indent_style = ParagraphStyle(
        'SubIndented', parent=body_style,
        leftIndent=48, spaceAfter=3,
    )
    sig_style = ParagraphStyle(
        'Signature', parent=styles['Normal'],
        fontSize=10, fontName='Times-Roman',
        spaceBefore=6, spaceAfter=2,
    )
    small_style = ParagraphStyle(
        'SmallPrint', parent=body_style,
        fontSize=8, leading=10, textColor=colors.Color(0.3, 0.3, 0.3),
    )

    story = []

    # ── Header ──
    story.append(Paragraph("INDEPENDENT CONTRACTOR SERVICES AGREEMENT", title_style))
    story.append(Paragraph("Nexus Digital Solutions LLC — Professional Services Contract", subtitle_style))
    story.append(Spacer(1, 4))

    # ── Preamble ──
    story.append(Paragraph(
        'This Independent Contractor Services Agreement (the "<b>Agreement</b>") is entered into as of '
        'March 1, 2026 (the "<b>Effective Date</b>"), by and between:', body_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        '<b>Nexus Digital Solutions LLC</b>, a Delaware limited liability company with its principal '
        'place of business at 1200 Innovation Drive, Suite 400, Wilmington, DE 19801 '
        '(hereinafter referred to as "<b>Client</b>" or "<b>Company</b>"), and', indent_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'The undersigned independent contractor (hereinafter referred to as "<b>Contractor</b>").', indent_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'WHEREAS, Client desires to engage Contractor to perform certain website redesign and '
        'development services; and WHEREAS, Contractor represents that Contractor has the requisite '
        'skills and experience to perform such services; NOW, THEREFORE, in consideration of the '
        'mutual covenants and agreements set forth herein, the parties agree as follows:', body_style))

    # ── Section 1: Scope of Services ──
    story.append(Paragraph("1. SCOPE OF SERVICES", heading_style))
    story.append(Paragraph(
        '1.1. Contractor shall perform website redesign and development services for Client\'s '
        'corporate website (the "<b>Project</b>"), including but not limited to: user interface design, '
        'front-end development, back-end integration, content migration, quality assurance testing, '
        'and deployment to production environment.', body_style))
    story.append(Paragraph(
        '1.2. The Project shall be completed in accordance with the specifications outlined in '
        'Exhibit A (attached hereto and incorporated by reference), as may be modified by Client '
        'from time to time in its sole discretion.', body_style))
    # TRAP: Unlimited revisions buried here
    story.append(Paragraph(
        '1.3. Contractor shall provide all necessary revisions, modifications, and adjustments '
        'to deliverables at no additional cost until Client confirms full satisfaction with '
        'the final output. There shall be no limitation on the number of revision cycles, and '
        'Contractor acknowledges that iterative refinement is an inherent component of the '
        'creative development process contemplated under this Agreement.', body_style))
    story.append(Paragraph(
        '1.4. Contractor shall devote sufficient time and resources to ensure timely completion '
        'of the Project and shall be available for reasonable consultation during Client\'s '
        'standard business hours.', body_style))

    # ── Section 2: Compensation ──
    story.append(Paragraph("2. COMPENSATION AND PAYMENT", heading_style))
    story.append(Paragraph(
        '2.1. In consideration for the services rendered hereunder, Client shall pay Contractor a '
        'total project fee of Fifteen Thousand Dollars ($15,000.00), payable in milestone installments '
        'as follows:', body_style))

    milestone_data = [
        ['Milestone', 'Deliverable', 'Amount'],
        ['Phase 1', 'Project kickoff and wireframes', '$3,000.00'],
        ['Phase 2', 'Design mockups and approval', '$4,000.00'],
        ['Phase 3', 'Development and integration', '$5,000.00'],
        ['Phase 4', 'Testing, launch, and handoff', '$3,000.00'],
    ]
    t = Table(milestone_data, colWidths=[1.2*inch, 3*inch, 1.3*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.15, 0.15, 0.25)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.7, 0.7, 0.7)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.Color(0.95, 0.95, 0.95), colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(Spacer(1, 6))
    story.append(t)
    story.append(Spacer(1, 6))

    # TRAP: Net 90 + withholding
    story.append(Paragraph(
        '2.2. Payment for each milestone shall be due within ninety (90) days following Client\'s '
        'receipt of a proper invoice from Contractor. Client reserves the right to withhold payment '
        'for any deliverable that Client determines, in its reasonable judgment, to be unsatisfactory '
        'or not in conformance with the Project specifications.', body_style))
    story.append(Paragraph(
        '2.3. Contractor shall be solely responsible for all taxes, insurance, and other obligations '
        'arising from compensation received under this Agreement. Client shall not withhold any '
        'taxes from payments made to Contractor.', body_style))
    story.append(Paragraph(
        '2.4. The fees set forth in Section 2.1 constitute the entire compensation payable to '
        'Contractor for all services performed under this Agreement, including all revisions '
        'contemplated in Section 1.3.', body_style))

    # ── Section 3: Intellectual Property ──
    story.append(Paragraph("3. INTELLECTUAL PROPERTY RIGHTS", heading_style))
    # TRAP: IP ownership including pre-existing IP + work for hire + moral rights waiver
    story.append(Paragraph(
        '3.1. All work product, deliverables, materials, designs, code, documentation, graphics, '
        'and any other output created by Contractor in connection with the Project, including '
        'without limitation all preliminary drafts, concepts, sketches, prototypes, and '
        'intermediate materials (collectively, "<b>Work Product</b>"), shall be considered '
        '"work made for hire" as defined under the United States Copyright Act (17 U.S.C. '
        '\u00a7 101). To the extent that any Work Product does not qualify as work made for hire, '
        'Contractor hereby irrevocably assigns to Client all right, title, and interest in and '
        'to such Work Product, including all intellectual property rights therein.', body_style))
    story.append(Paragraph(
        '3.2. The assignment in Section 3.1 includes, without limitation, any pre-existing '
        'intellectual property, tools, frameworks, libraries, code snippets, templates, or '
        'methodologies that Contractor incorporates into or utilizes in the creation of the '
        'Work Product (collectively, "<b>Contractor Materials</b>"). Contractor represents and '
        'warrants that Contractor has full authority to assign such Contractor Materials.', body_style))
    story.append(Paragraph(
        '3.3. Contractor hereby irrevocably waives, to the fullest extent permitted by applicable '
        'law, all moral rights (including rights of attribution and integrity) in and to the '
        'Work Product worldwide and in perpetuity, and agrees not to assert any such rights '
        'against Client or its successors, assigns, or licensees.', body_style))

    # ── Section 4: Confidentiality ──
    story.append(Paragraph("4. CONFIDENTIALITY AND NON-DISCLOSURE", heading_style))
    story.append(Paragraph(
        '4.1. Contractor acknowledges that during the course of this engagement, Contractor may '
        'have access to confidential and proprietary information of Client, including but not '
        'limited to business strategies, customer data, financial information, technical '
        'specifications, and trade secrets (collectively, "<b>Confidential Information</b>").', body_style))
    story.append(Paragraph(
        '4.2. Contractor shall not, during the term of this Agreement or at any time thereafter, '
        'disclose, publish, or otherwise disseminate any Confidential Information to any third '
        'party without the prior written consent of Client.', body_style))
    # TRAP: No portfolio use, can't even say they worked with Client
    story.append(Paragraph(
        '4.3. Contractor shall not, at any time during or after the term of this Agreement, '
        'disclose the existence of this Agreement or the business relationship between the '
        'parties to any third party. Contractor further agrees that Contractor shall not use '
        'any Work Product, deliverables, or reference to the Project in Contractor\'s portfolio, '
        'website, social media, marketing materials, or any other public or private communication '
        'without the express prior written consent of Client, which may be withheld in Client\'s '
        'sole and absolute discretion.', body_style))

    # ── Section 5: Non-Competition ──
    story.append(Paragraph("5. NON-COMPETITION AND NON-SOLICITATION", heading_style))
    # TRAP: 24-month, "technology industry," no geographic limit
    story.append(Paragraph(
        '5.1. During the term of this Agreement and for a period of twenty-four (24) months '
        'following its termination or expiration (the "<b>Restricted Period</b>"), Contractor '
        'shall not, directly or indirectly, engage in, own, manage, operate, control, be employed '
        'by, participate in, consult for, or be connected with any business or activity that is '
        'competitive with Client\'s business within the technology industry.', body_style))
    story.append(Paragraph(
        '5.2. During the Restricted Period, Contractor shall not, directly or indirectly, '
        'solicit, contact, or attempt to solicit any client, customer, vendor, or business '
        'partner of Client for the purpose of providing services similar to those provided '
        'under this Agreement.', body_style))

    # ── Section 6: Term and Termination ──
    story.append(Paragraph("6. TERM, TERMINATION, AND RENEWAL", heading_style))
    story.append(Paragraph(
        '6.1. This Agreement shall commence on the Effective Date and shall continue for an '
        'initial term of twelve (12) months (the "<b>Initial Term</b>").', body_style))
    # TRAP: Auto-renewal with 120-day cancellation window
    story.append(Paragraph(
        '6.2. Upon expiration of the Initial Term, this Agreement shall automatically renew '
        'for successive periods of twelve (12) months each (each a "<b>Renewal Term</b>"), '
        'unless either party provides written notice of non-renewal at least one hundred '
        'twenty (120) days prior to the expiration of the then-current term.', body_style))
    # TRAP: One-sided termination
    story.append(Paragraph(
        '6.3. Client may terminate this Agreement at any time, with or without cause, '
        'effective immediately upon written notice to Contractor. In the event of termination '
        'by Client under this Section, Client shall have no obligation to compensate Contractor '
        'for any work in progress or incomplete deliverables.', body_style))
    story.append(Paragraph(
        '6.4. Contractor may terminate this Agreement only upon ninety (90) days\' prior '
        'written notice to Client. During such notice period, Contractor shall continue to '
        'perform all obligations under this Agreement and shall cooperate fully in the '
        'transition of the Project to a replacement contractor designated by Client.', body_style))
    # TRAP: No kill fee
    story.append(Paragraph(
        '6.5. In the event of cancellation or termination of the Project for any reason, '
        'Contractor acknowledges and agrees that Contractor shall not be entitled to any '
        'compensation for work performed prior to the effective date of termination, except '
        'for milestone payments that have been previously approved and invoiced in accordance '
        'with Section 2.', body_style))

    # ── Section 7: Indemnification ──
    story.append(Paragraph("7. INDEMNIFICATION", heading_style))
    # TRAP: One-sided indemnification including Client's own negligence
    story.append(Paragraph(
        '7.1. Contractor shall indemnify, defend, and hold harmless Client and its officers, '
        'directors, employees, agents, successors, and assigns from and against any and all '
        'claims, damages, losses, liabilities, costs, and expenses (including reasonable '
        'attorneys\' fees) arising out of or relating to: (a) Contractor\'s performance or '
        'failure to perform under this Agreement; (b) any breach of any representation, '
        'warranty, or covenant made by Contractor; (c) any negligent or wrongful act or '
        'omission of Contractor or any person acting under Contractor\'s direction; or '
        '(d) any claim by a third party related to the Work Product or services provided '
        'hereunder, regardless of whether such claim arises in whole or in part from the '
        'negligence or acts of Client.', body_style))
    story.append(Paragraph(
        '7.2. Contractor\'s indemnification obligations under this Section shall survive the '
        'termination or expiration of this Agreement indefinitely.', body_style))

    # ── Section 8: Limitation of Liability ──
    story.append(Paragraph("8. LIMITATION OF LIABILITY", heading_style))
    # TRAP: Client liability capped at 30 days of fees, Contractor unlimited
    story.append(Paragraph(
        '8.1. IN NO EVENT SHALL CLIENT BE LIABLE TO CONTRACTOR FOR ANY INDIRECT, INCIDENTAL, '
        'SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF OR RELATED TO THIS '
        'AGREEMENT, REGARDLESS OF THE THEORY OF LIABILITY.', body_style))
    story.append(Paragraph(
        '8.2. CLIENT\'S TOTAL AGGREGATE LIABILITY UNDER THIS AGREEMENT SHALL NOT EXCEED THE '
        'AMOUNT OF FEES ACTUALLY PAID BY CLIENT TO CONTRACTOR DURING THE THIRTY (30) DAY '
        'PERIOD IMMEDIATELY PRECEDING THE EVENT GIVING RISE TO THE CLAIM.', body_style))
    story.append(Paragraph(
        '8.3. The limitations set forth in Sections 8.1 and 8.2 shall apply to Client only. '
        'Contractor acknowledges that Contractor\'s liability under this Agreement shall not '
        'be subject to any cap or limitation.', body_style))

    # ── Section 9: Representations and Warranties ──
    story.append(Paragraph("9. REPRESENTATIONS AND WARRANTIES", heading_style))
    story.append(Paragraph(
        '9.1. Contractor represents and warrants that: (a) Contractor has the right, power, '
        'and authority to enter into this Agreement; (b) the Work Product will be original '
        'and will not infringe upon any intellectual property rights of any third party; '
        '(c) Contractor will perform the services in a professional and workmanlike manner; '
        'and (d) Contractor is an independent contractor and not an employee of Client.', body_style))
    story.append(Paragraph(
        '9.2. CLIENT MAKES NO WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO '
        'ANY IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, WITH '
        'RESPECT TO ANY MATERIALS, SPECIFICATIONS, OR INFORMATION PROVIDED TO CONTRACTOR.', body_style))

    # ── Section 10: Governing Law ──
    story.append(Paragraph("10. GOVERNING LAW AND DISPUTE RESOLUTION", heading_style))
    # TRAP: BVI jurisdiction, no mediation/arbitration
    story.append(Paragraph(
        '10.1. This Agreement shall be governed by and construed in accordance with the laws '
        'of the British Virgin Islands, without regard to its conflict of laws principles.', body_style))
    story.append(Paragraph(
        '10.2. Any dispute, controversy, or claim arising out of or relating to this Agreement '
        'shall be resolved exclusively in the courts of the British Virgin Islands, and each '
        'party hereby irrevocably submits to the personal jurisdiction of such courts and waives '
        'any objection to venue therein.', body_style))
    story.append(Paragraph(
        '10.3. In the event of any legal action arising under this Agreement, the prevailing '
        'party shall be entitled to recover its reasonable attorneys\' fees and costs from '
        'the non-prevailing party.', body_style))

    # ── Section 11: General Provisions ──
    story.append(Paragraph("11. GENERAL PROVISIONS", heading_style))
    story.append(Paragraph(
        '11.1. <b>Entire Agreement.</b> This Agreement, together with all exhibits and '
        'attachments hereto, constitutes the entire agreement between the parties with respect '
        'to the subject matter hereof and supersedes all prior and contemporaneous agreements, '
        'understandings, negotiations, and discussions, whether oral or written.', body_style))
    story.append(Paragraph(
        '11.2. <b>Amendments.</b> This Agreement may not be amended or modified except by a '
        'written instrument signed by both parties; provided, however, that Client may modify '
        'the Project specifications set forth in Exhibit A at any time upon written notice '
        'to Contractor.', body_style))
    story.append(Paragraph(
        '11.3. <b>Severability.</b> If any provision of this Agreement is held to be invalid '
        'or unenforceable, the remaining provisions shall continue in full force and effect.', body_style))
    story.append(Paragraph(
        '11.4. <b>Waiver.</b> The failure of either party to enforce any provision of this '
        'Agreement shall not constitute a waiver of such party\'s right to enforce such '
        'provision in the future.', body_style))
    story.append(Paragraph(
        '11.5. <b>Assignment.</b> Contractor may not assign or transfer this Agreement or any '
        'rights hereunder without the prior written consent of Client. Client may freely '
        'assign this Agreement to any successor or affiliate.', body_style))
    story.append(Paragraph(
        '11.6. <b>Notices.</b> All notices under this Agreement shall be in writing and shall '
        'be deemed given when delivered personally, sent by certified mail (return receipt '
        'requested), or sent by recognized overnight courier to the addresses set forth above.', body_style))
    story.append(Paragraph(
        '11.7. <b>Survival.</b> Sections 3, 4, 5, 7, 8, and 10 shall survive the termination '
        'or expiration of this Agreement.', body_style))

    story.append(Spacer(1, 30))

    # ── Signature Block ──
    story.append(Paragraph(
        'IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date '
        'first written above.', body_style))
    story.append(Spacer(1, 20))

    sig_data = [
        ['NEXUS DIGITAL SOLUTIONS LLC', '', 'CONTRACTOR'],
        ['', '', ''],
        ['Signature: ____________________________', '', 'Signature: ____________________________'],
        ['Name: Marcus J. Whitfield', '', 'Name: ____________________________'],
        ['Title: Chief Operating Officer', '', 'Title: ____________________________'],
        ['Date: ____________________________', '', 'Date: ____________________________'],
    ]
    sig_table = Table(sig_data, colWidths=[2.8*inch, 0.4*inch, 2.8*inch])
    sig_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(sig_table)

    story.append(Spacer(1, 30))
    story.append(Paragraph(
        '<i>This document contains confidential and proprietary information. '
        'Unauthorized distribution or reproduction is strictly prohibited. '
        'Document ID: NDS-PSA-2026-00847</i>', small_style))

    # Build
    doc.build(story)
    print(f"Contract PDF generated: {OUTPUT_PATH}")
    print(f"File size: {os.path.getsize(OUTPUT_PATH):,} bytes")


if __name__ == "__main__":
    build_contract()
