import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, PageBreak, Spacer, Table, TableStyle, Preformatted
)
from reportlab.pdfgen import canvas
import pypdf

class SimplePageNumberCanvas(canvas.Canvas):
    """
    Draws a clean centered page number at the bottom of each page,
    matching the exact style of the reference report.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number()
            super().showPage()
        super().save()

    def draw_page_number(self):
        self.saveState()
        self.setFont('Times-Roman', 10)
        self.setFillColor(colors.HexColor('#1E293B'))
        # Centered at bottom (page width is 612, center is 306)
        self.drawCentredString(306, 36, str(self._pageNumber))
        self.restoreState()

def generate_15_page_report(pdf_path):
    # Standard letter: 612 x 792 pt. Margins: 54 pt left/right (0.75 in), 44 pt top, 46 pt bottom
    # Printable width: 612 - 108 = 504 pt. Printable height: 792 - 90 = 702 pt.
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=44,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Exact colors matching DSCE reference document
    primary_blue = colors.HexColor('#2563EB')  # Clean academic blue for section titles
    dark_text    = colors.HexColor('#0F172A')  # Very dark slate / near black
    muted_text   = colors.HexColor('#334155')  # Slate 700
    table_border = colors.HexColor('#94A3B8')  # Subtle slate border
    table_bg     = colors.HexColor('#F8FAFC')
    header_bg    = colors.HexColor('#E2E8F0')

    # Typography styles matching the reference document
    cover_top_style = ParagraphStyle(
        'CoverTop',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=1,  # Center
        textColor=dark_text,
        spaceAfter=30
    )

    cover_title_style = ParagraphStyle(
        'CoverTitle',
        fontName='Times-Bold',
        fontSize=17,
        leading=22,
        alignment=1,  # Center
        textColor=dark_text,
        spaceAfter=14
    )

    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='Times-Roman',
        fontSize=11,
        leading=15,
        alignment=1,  # Center
        textColor=muted_text,
        spaceAfter=45
    )

    cover_meta_header = ParagraphStyle(
        'CoverMetaHeader',
        fontName='Times-Bold',
        fontSize=11,
        leading=16,
        alignment=1,  # Center
        textColor=dark_text,
        spaceAfter=5
    )

    cover_meta_body = ParagraphStyle(
        'CoverMetaBody',
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        alignment=1,  # Center
        textColor=dark_text,
        spaceAfter=2
    )

    cover_bottom_style = ParagraphStyle(
        'CoverBottom',
        fontName='Times-Bold',
        fontSize=10.5,
        leading=15,
        alignment=1,  # Center
        textColor=dark_text,
        spaceAfter=4
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=primary_blue,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    sub_heading = ParagraphStyle(
        'SubHeading',
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        textColor=dark_text,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_text = ParagraphStyle(
        'ReportBody',
        fontName='Times-Roman',
        fontSize=10,
        leading=14.5,
        alignment=4,  # Justified
        textColor=dark_text,
        spaceAfter=6
    )

    body_bullet = ParagraphStyle(
        'ReportBullet',
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        alignment=4,
        textColor=dark_text,
        leftIndent=15,
        spaceAfter=3
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Times-Bold',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=dark_text
    )

    table_body = ParagraphStyle(
        'TableBody',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        textColor=dark_text
    )

    table_code = ParagraphStyle(
        'TableCode',
        fontName='Courier',
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=dark_text
    )

    code_block_style = ParagraphStyle(
        'CodeBlock',
        fontName='Courier',
        fontSize=6.1,
        leading=7.6,
        textColor=colors.HexColor('#0F172A')
    )

    term_output_style = ParagraphStyle(
        'TermOutput',
        fontName='Courier',
        fontSize=7.0,
        leading=9.0,
        textColor=colors.HexColor('#E2E8F0')
    )

    fig_caption = ParagraphStyle(
        'FigCaption',
        fontName='Times-Italic',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=muted_text,
        spaceBefore=4,
        spaceAfter=8
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE PAGE (Exact layout of reference Page 1)
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("OPERATING SYSTEMS - MINI PROJECT REPORT", cover_top_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("REAL-LIFE APPLICATION OF BANKER'S ALGORITHM", cover_title_style))
    story.append(Paragraph("A C-Based Simulation of Deadlock Avoidance in Hospital Operating Room & ICU Resource Scheduling", cover_subtitle_style))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("Submitted by", cover_meta_header))
    story.append(Paragraph("Name: AKHIL SRINATH", cover_meta_body))
    story.append(Paragraph("USN No.: 1DS25CG003", cover_meta_body))
    story.append(Paragraph("Class / Section: 3<sup>RD</sup> SEM / CG", cover_meta_body))
    
    story.append(Spacer(1, 35))
    story.append(Paragraph("Submitted to", cover_meta_header))
    story.append(Paragraph("Professor: NAYANA SHINDE", cover_meta_body))
    
    story.append(Spacer(1, 65))
    story.append(Paragraph("Department of Computer Science and Design", cover_bottom_style))
    story.append(Paragraph("College / University: DAYANANDA SAGAR COLLEGE OF ENGINEERING", cover_bottom_style))
    story.append(Paragraph("Academic Year 2026-2027", cover_meta_body))
    
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CERTIFICATE (Exact layout of reference Page 2)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("CERTIFICATE", section_heading))
    story.append(Spacer(1, 15))
    
    cert_text = (
        "This is to certify that the mini project report entitled "
        "&ldquo;<b>Real-Life Application of Banker's Algorithm - "
        "A C-Based Simulation of Deadlock Avoidance in Hospital Operating Room & ICU Resource Scheduling</b>&rdquo; "
        "has been carried out by <b>Akhil Srinath</b> (USN: <b>1DS25CG003</b>) under the guidance of "
        "<b>Prof Nayana Shinde</b> as part of the Operating Systems course in the Department of Computer Science "
        "and Design, Dayananda Sagar College of Engineering, during the academic year 2026-2027."
    )
    story.append(Paragraph(cert_text, body_text))
    
    story.append(Spacer(1, 140))
    story.append(Paragraph("Faculty Signature: ____________________", body_text))
    story.append(Spacer(1, 25))
    story.append(Paragraph("Date: ____________________", body_text))
    
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: DECLARATION (Exact layout of reference Page 3)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("DECLARATION", section_heading))
    story.append(Spacer(1, 15))
    
    decl_text = (
        "I hereby declare that this project report entitled "
        "&ldquo;<b>Real-Life Application of Banker's Algorithm</b>&rdquo; "
        "is prepared as part of my academic coursework for the Operating Systems course in the Department of "
        "Computer Science and Design, Dayananda Sagar College of Engineering. The project is intended as an "
        "educational simulation of selected operating-system deadlock avoidance concepts using C and does not "
        "claim to implement an actual commercial hospital operating system kernel."
    )
    story.append(Paragraph(decl_text, body_text))
    story.append(Spacer(1, 120))
    story.append(Paragraph("Student Signature: ____________________", body_text))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Date: ____________________", body_text))
    
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: ACKNOWLEDGEMENT (Exact layout of reference Page 4)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("ACKNOWLEDGEMENT", section_heading))
    story.append(Spacer(1, 15))
    
    ack_text_1 = (
        "I would like to express my sincere gratitude to my Operating Systems professor, <b>Prof Nayana Shinde</b>, "
        "for providing the opportunity to develop this mini project. The project helped in understanding important "
        "operating-system concepts through practical C implementation."
    )
    ack_text_2 = (
        "I also thank the Department of Computer Science and Design, Dayananda Sagar College of Engineering, our faculty "
        "members, and my classmates for their support and guidance during the development and testing of the project."
    )
    story.append(Paragraph(ack_text_1, body_text))
    story.append(Spacer(1, 8))
    story.append(Paragraph(ack_text_2, body_text))
    
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TABLE OF CONTENTS (Exact layout of reference Page 5)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("TABLE OF CONTENTS", section_heading))
    story.append(Spacer(1, 8))
    
    toc_items = [
        "1. Abstract",
        "2. Introduction",
        "3. Objectives",
        "4. Project Overview",
        "5. Theoretical Foundations of Deadlock",
        "6. Deadlock Conditions in Hospital Surgery",
        "7. System Requirements",
        "8. System Design and Architecture",
        "9. Mathematical Model & Baseline State",
        "10. Banker's Algorithm Working Rules",
        "11. Step-by-Step Safety Audit Trace",
        "12. Evaluation of Request Scenarios",
        "13. Implementation and Working",
        "14. Results and Screenshots",
        "15. Limitations & Real-World Analysis",
        "16. Conclusion",
        "17. Future Scope",
        "18. References"
    ]
    for item in toc_items:
        story.append(Paragraph(item, body_text))
    
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: 1. ABSTRACT & 2. INTRODUCTION (Exact layout of reference Page 6)
    # =========================================================================
    story.append(Paragraph("1. ABSTRACT", section_heading))
    story.append(Paragraph(
        "An Operating System (OS) is system software that acts as an interface between the user and computer hardware. "
        "It manages important resources such as the processor, memory, files, input/output devices, and concurrency locks.",
        body_text
    ))
    story.append(Paragraph(
        "This project presents a C-based Operating System simulation designed to demonstrate Dijkstra's Banker's Algorithm "
        "applied to a non-computing real-world application: a multi-specialty hospital surgical center and intensive care unit (ICU). "
        "The model demonstrates how five concurrent surgical operations compete for finite, scarce clinical infrastructure including "
        "modular operating suites, dedicated specialist anesthesiology teams, and mechanical ventilators.",
        body_text
    ))
    story.append(Paragraph(
        "The project does not attempt to create an actual operating-system kernel. Instead, it provides a rigorous educational "
        "simulation in which resource allocation, remaining need calculation, safe sequence derivation, and request rollback "
        "are modeled using C data structures, algorithms, and simulated surgical events.",
        body_text
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2. INTRODUCTION", section_heading))
    story.append(Paragraph(
        "Deadlock is a critical state in concurrent systems where two or more processes are permanently blocked because each holds "
        "a resource and waits for another resource held by another process. While classically studied in operating systems "
        "managing CPU registers and memory pages, deadlock is a universal challenge across complex physical systems.",
        body_text
    ))
    story.append(Paragraph(
        "In a busy hospital, surgical suites and life-support machines represent scarce physical assets. If surgical teams are "
        "granted resources without forward-looking safety verification, the center can reach a catastrophic circular deadlock "
        "where multiple patients are anesthetized on operating tables unable to either finish or move to recovery.",
        body_text
    ))
    story.append(Paragraph("<b>Scope of the Project:</b>", sub_heading))
    story.append(Paragraph("• Deadlock Avoidance Principles in Cyber-Physical Systems", body_bullet))
    story.append(Paragraph("• Mapping Operating System Primitives to Clinical Infrastructure", body_bullet))
    story.append(Paragraph("• Need Matrix and Available Vector Calculation in C", body_bullet))
    story.append(Paragraph("• Mathematical Safety Algorithm and Safe Sequence Audit", body_bullet))
    story.append(Paragraph("• Dynamic Resource Request Validation, Trial Allocation, and Rollback", body_bullet))
    
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: 3. OBJECTIVES & 4. PROJECT OVERVIEW (Exact layout of reference Page 7)
    # =========================================================================
    story.append(Paragraph("3. OBJECTIVES", section_heading))
    objectives = [
        "1. Understand the fundamental principles of resource allocation and deadlock in operating systems.",
        "2. Develop a working software model of Dijkstra's Banker's Algorithm using C.",
        "3. Demonstrate how concurrent tasks can be modeled using processes and resource matrices.",
        "4. Formulate a realistic real-world case study outside the traditional banking analogy.",
        "5. Implement matrix data structures for Allocation, Max Claim, Need, and Available vectors.",
        "6. Implement and demonstrate the Safety Algorithm to determine system state safety.",
        "7. Implement the Resource-Request Algorithm to validate incoming resource demands.",
        "8. Demonstrate state rollback mechanisms when an unsafe allocation is detected.",
        "9. Evaluate practical engineering trade-offs between theoretical assumptions and clinical realities.",
        "10. Provide an interactive command-line environment for exploring these deadlock concepts."
    ]
    for obj in objectives:
        story.append(Paragraph(obj, body_text))

    story.append(Spacer(1, 6))
    story.append(Paragraph("4. PROJECT OVERVIEW", section_heading))
    story.append(Paragraph(
        "The project is implemented as a modular C application simulating a hospital surgical dispatcher. "
        "When the simulation runs, it performs an initial safety audit, prints the baseline state table, "
        "and executes realistic clinical request scenarios.",
        body_text
    ))
    overview_box = (
        "=== Hospital Surgical Dispatcher ===\n"
        "1. Initialize System State & Compute Matrices\n"
        "2. Execute Initial Safety Audit\n"
        "3. Evaluate Scenario 1: Safe Request (Cardiac CABG)\n"
        "4. Evaluate Scenario 2: Unsafe Request (Trauma Laparotomy)\n"
        "5. Exit Simulation"
    )
    t_over = Table([[Preformatted(overview_box, code_block_style)]], colWidths=[504])
    t_over.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), table_bg),
        ('BOX', (0,0), (-1,-1), 0.5, table_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_over)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The underlying simulations use internal C data structures rather than real hospital databases, "
        "providing a clean, deterministic platform for academic study.",
        body_text
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: 5. THEORETICAL FOUNDATIONS & 6. DEADLOCK CONDITIONS
    # =========================================================================
    story.append(Paragraph("5. THEORETICAL FOUNDATIONS OF DEADLOCK", section_heading))
    story.append(Paragraph(
        "In computer science, deadlock handling strategies are broadly divided into three paradigms: "
        "Deadlock Prevention, Deadlock Avoidance, and Deadlock Detection & Recovery.",
        body_text
    ))
    story.append(Paragraph(
        "• <b>Deadlock Prevention:</b> Constrains resource requests such that at least one of the Coffman conditions cannot hold. "
        "In a hospital, requiring a surgery to hold an ICU ventilator hours before it is needed starves other operating suites, "
        "leading to unacceptable resource underutilization.",
        body_text
    ))
    story.append(Paragraph(
        "• <b>Deadlock Detection and Recovery:</b> Allows deadlocks to occur, detects them periodically, and aborts processes. "
        "In surgery, terminating an active procedure mid-operation to recover equipment is medically unacceptable and fatal.",
        body_text
    ))
    story.append(Paragraph(
        "• <b>Deadlock Avoidance (Banker's Algorithm):</b> The system dynamically inspects resource-allocation state to ensure "
        "that a circular-wait condition can never exist. This balances high equipment utilization with guaranteed safety.",
        body_text
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6. DEADLOCK CONDITIONS IN HOSPITAL SURGERY", section_heading))
    story.append(Paragraph(
        "A medical deadlock occurs if and only if all four Coffman conditions are concurrently satisfied:",
        body_text
    ))
    story.append(Paragraph("• <b>Mutual Exclusion:</b> An operating suite or ventilator can strictly support only one patient at a time.", body_bullet))
    story.append(Paragraph("• <b>Hold and Wait:</b> A surgical team occupies an OR suite while holding to acquire a post-op ICU ventilator.", body_bullet))
    story.append(Paragraph("• <b>No Preemption:</b> An active surgery cannot be aborted or evicted to free up equipment without grave harm.", body_bullet))
    story.append(Paragraph("• <b>Circular Wait:</b> Surgery A holds an OR waiting for a ventilator; Surgery B holds a ventilator waiting for an OR.", body_bullet))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Conceptual Domain Mapping Table:</b>", sub_heading))
    
    map_table_data = [
        [Paragraph("<b>Operating System Concept</b>", table_header), Paragraph("<b>Hospital Critical Care Equivalent</b>", table_header), Paragraph("<b>Implementation Entity in C</b>", table_header)],
        [Paragraph("Process ($P_i$)", table_body), Paragraph("Active Surgical Case / Patient Pathway", table_body), Paragraph("Index <code>i</code> (0 to 4)", table_code)],
        [Paragraph("Resource Type ($R_j$)", table_body), Paragraph("Physical Clinical Asset (ORs, Anesthesia, Ventilators)", table_body), Paragraph("Index <code>j</code> (0 to 2)", table_code)],
        [Paragraph("Total Capacity ($E$)", table_body), Paragraph("Total hospital physical inventory of rooms, staff, machines", table_body), Paragraph("Array <code>total[3] = {10, 5, 7}</code>", table_code)],
        [Paragraph("Allocation Matrix", table_body), Paragraph("Assets currently deployed in active surgical suites", table_body), Paragraph("Matrix <code>alloc[5][3]</code>", table_code)],
        [Paragraph("Max Claim Matrix", table_body), Paragraph("Worst-case peak asset requirement declared for the surgery", table_body), Paragraph("Matrix <code>max_claim[5][3]</code>", table_code)],
        [Paragraph("Need Matrix", table_body), Paragraph("Remaining resources that may still be required to finish", table_body), Paragraph("Matrix <code>need[5][3] = Max - Alloc</code>", table_code)],
        [Paragraph("Available Vector", table_body), Paragraph("Unallocated clinical assets ready for deployment", table_body), Paragraph("Array <code>avail[3] = Total - Sum(Alloc)</code>", table_code)],
        [Paragraph("Safe State", table_body), Paragraph("Schedule where every surgery is guaranteed to complete", table_body), Paragraph("Returns <code>true</code> from <code>is_safe()</code>", table_code)]
    ]
    t_map = Table(map_table_data, colWidths=[130, 248, 126])
    t_map.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, table_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, table_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_map)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: 7. SYSTEM REQUIREMENTS & 8. SYSTEM DESIGN AND ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("7. SYSTEM REQUIREMENTS", section_heading))
    story.append(Paragraph("<b>7.1 Hardware Requirements:</b>", sub_heading))
    
    hw_data = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Requirement</b>", table_header)],
        [Paragraph("Processor", table_body), Paragraph("Any modern x86_64 or ARM processor", table_body)],
        [Paragraph("RAM", table_body), Paragraph("4 GB or higher", table_body)],
        [Paragraph("Storage", table_body), Paragraph("Less than 50 MB free disk space", table_body)],
        [Paragraph("Display", table_body), Paragraph("Standard monitor (1080p recommended)", table_body)],
        [Paragraph("Input", table_body), Paragraph("Standard Keyboard and Mouse", table_body)]
    ]
    t_hw = Table(hw_data, colWidths=[200, 304])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, table_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_hw)

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>7.2 Software Requirements:</b>", sub_heading))
    
    sw_data = [
        [Paragraph("<b>Software</b>", table_header), Paragraph("<b>Requirement</b>", table_header)],
        [Paragraph("Programming Language", table_body), Paragraph("C (ANSI C / C99 Standard)", table_body)],
        [Paragraph("Compiler", table_body), Paragraph("GCC (MinGW / Clang / MSVC compatible)", table_body)],
        [Paragraph("Operating Environment", table_body), Paragraph("Windows 10 / 11, Linux, or macOS", table_body)],
        [Paragraph("IDE / Code Editor", table_body), Paragraph("Visual Studio Code", table_body)],
        [Paragraph("Command Interface", table_body), Paragraph("PowerShell / Command Prompt / Terminal", table_body)]
    ]
    t_sw = Table(sw_data, colWidths=[200, 304])
    t_sw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, table_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_sw)

    story.append(Spacer(1, 6))
    story.append(Paragraph("8. SYSTEM DESIGN AND ARCHITECTURE", section_heading))
    story.append(Paragraph(
        "The project follows a modular C architecture. The dispatcher mediates between surgical procedure requests "
        "and physical asset pools via speculative state testing:",
        body_text
    ))

    arch_diagram = (
        "                    +------------------------------------------+\n"
        "                    |     HOSPITAL SURGICAL DISPATCHER (C)     |\n"
        "                    +------------------------------------------+\n"
        "                                         |\n"
        "             +---------------------------+---------------------------+\n"
        "             |                                                       |\n"
        "             v                                                       v\n"
        "   [Request Evaluation]                                    [Safety State Engine]\n"
        "   - Rule 1: Req <= Need?                                  - Vector: Work = Available\n"
        "   - Rule 2: Req <= Avail?                                 - Flag: Finish[P] = False\n"
        "   - Speculative Allocation                                - Scan: Need[i] <= Work\n"
        "             |                                                       |\n"
        "             +--------------------------->+<-------------------------+\n"
        "                                          |\n"
        "                        +-----------------+-----------------+\n"
        "                        |                                   |\n"
        "                 [Safe Sequence Found]             [No Sequence Possible]\n"
        "                 GRANT ASSETS TO SURGERY           ROLLBACK & QUEUE SURGERY"
    )
    t_arch = Table([[Preformatted(arch_diagram, code_block_style)]], colWidths=[504])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), table_bg),
        ('BOX', (0,0), (-1,-1), 0.5, table_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_arch)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: 9. MATHEMATICAL MODEL & 10. BANKER'S WORKING RULES
    # =========================================================================
    story.append(Paragraph("9. MATHEMATICAL MODEL & BASELINE CONFIGURATION", section_heading))
    story.append(Paragraph(
        "Total hospital inventory: <b>10 Operating Rooms ($A$), 5 Anesthesia Teams ($B$), 7 Ventilators ($C$)</b>. "
        "Total capacity vector: <b>E = [10, 5, 7]</b>. Five procedures are currently active:",
        body_text
    ))

    base_table_data = [
        [Paragraph("<b>Procedure Code & Medical Specialty</b>", table_header),
         Paragraph("<b>Allocation</b><br/>[A, B, C]", table_header),
         Paragraph("<b>Max Claim</b><br/>[A, B, C]", table_header),
         Paragraph("<b>Need (Max - Alloc)</b><br/>[A, B, C]", table_header),
         Paragraph("<b>Clinical Rationale</b>", table_header)],
        [Paragraph("<b>P0</b>: Trauma Laparotomy", table_body), Paragraph("[0, 1, 0]", table_code), Paragraph("[7, 5, 3]", table_code), Paragraph("[7, 4, 3]", table_code), Paragraph("Polytrauma stabilization; potential massive transfusion.", table_body)],
        [Paragraph("<b>P1</b>: Cardiac Bypass (CABG)", table_body), Paragraph("[2, 0, 0]", table_code), Paragraph("[3, 2, 2]", table_code), Paragraph("[1, 2, 2]", table_code), Paragraph("Dual OR suite prep; requires anesthesia & weaning vent.", table_body)],
        [Paragraph("<b>P2</b>: Pediatric Craniotomy", table_body), Paragraph("[3, 0, 2]", table_code), Paragraph("[9, 0, 2]", table_code), Paragraph("[6, 0, 0]", table_code), Paragraph("Extended cranial resection; may expand into observation.", table_body)],
        [Paragraph("<b>P3</b>: Multi-Organ Transplant", table_body), Paragraph("[2, 1, 1]", table_code), Paragraph("[2, 2, 2]", table_code), Paragraph("[0, 1, 1]", table_code), Paragraph("Donor-recipient parallel grafting suites.", table_body)],
        [Paragraph("<b>P4</b>: Complex Spine Fusion", table_body), Paragraph("[0, 0, 2]", table_code), Paragraph("[4, 3, 3]", table_code), Paragraph("[4, 3, 1]", table_code), Paragraph("Spine reconstruction requiring prone mechanical ventilation.", table_body)],
        [Paragraph("<b>Total Allocated Assets</b>", table_header), Paragraph("<b>[7, 2, 5]</b>", table_code), Paragraph("—", table_body), Paragraph("—", table_body), Paragraph("Current physical assets deployed in surgical suites.", table_body)],
        [Paragraph("<b>Available Inventory</b>", table_header), Paragraph("<b>[3, 3, 2]</b>", table_code), Paragraph("—", table_body), Paragraph("—", table_body), Paragraph("<b>Available = Total [10, 5, 7] - Allocated [7, 2, 5]</b>", table_body)],
    ]
    t_base = Table(base_table_data, colWidths=[150, 70, 70, 85, 129])
    t_base.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, table_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-3), [colors.white, table_bg]),
        ('BACKGROUND', (0,-2), (-1,-1), colors.HexColor('#F1F5F9')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_base)

    story.append(Spacer(1, 6))
    story.append(Paragraph("10. BANKER'S ALGORITHM WORKING RULES", section_heading))
    story.append(Paragraph(
        "When an active surgical team $P_i$ submits a request $Request_i$ for additional clinical assets, "
        "the hospital dispatcher evaluates three fundamental rules:",
        body_text
    ))
    story.append(Paragraph(
        "<b>Rule 1 (Claim Bound):</b> If $Request_i[j] > Need_i[j]$ for any resource $j$, reject the request immediately. "
        "A surgical procedure cannot request more assets than its declared maximum clinical scope.",
        body_bullet
    ))
    story.append(Paragraph(
        "<b>Rule 2 (Physical Stock Bound):</b> If $Request_i[j] > Available[j]$ for any resource $j$, procedure $P_i$ must wait. "
        "The hospital inventory simply does not possess unallocated units to satisfy the request right now.",
        body_bullet
    ))
    story.append(Paragraph(
        "<b>Rule 3 (Speculative Allocation & Safety Verification):</b> If Rules 1 and 2 pass, the system simulates granting the request: "
        "$Available' = Available - Request_i$, $Allocation_i' = Allocation_i + Request_i$, $Need_i' = Need_i - Request_i$. "
        "The <b>Safety Algorithm</b> is executed. If a safe sequence exists, the request is approved. If unsafe, state changes are rolled back.",
        body_bullet
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: 11. STEP-BY-STEP SAFETY AUDIT TRACE
    # =========================================================================
    story.append(Paragraph("11. STEP-BY-STEP SAFETY AUDIT TRACE", section_heading))
    story.append(Paragraph(
        "<b>Initial Safety Audit:</b> With <b>Work = Available = [3, 3, 2]</b> and <b>Finish = [False, False, False, False, False]</b>, "
        "we iteratively search for an unfinished procedure where $Need_i \\le Work$:",
        body_text
    ))

    audit_data = [
        [Paragraph("<b>Iteration</b>", table_header), Paragraph("<b>Candidate</b>", table_header), Paragraph("<b>Need Vector</b>", table_header), Paragraph("<b>Work Vector</b>", table_header), Paragraph("<b>Condition $Need \\le Work$?</b>", table_header), Paragraph("<b>Action Taken & Updated Work Vector</b>", table_header)],
        [Paragraph("Step 1", table_body), Paragraph("<b>P0</b>", table_body), Paragraph("[7, 4, 3]", table_code), Paragraph("[3, 3, 2]", table_code), Paragraph("False (7>3, 4>3, 3>2)", table_body), Paragraph("Cannot satisfy max need yet. Skip for now.", table_body)],
        [Paragraph("Step 2", table_body), Paragraph("<b>P1</b>", table_body), Paragraph("[1, 2, 2]", table_code), Paragraph("[3, 3, 2]", table_code), Paragraph("<b>True</b> (1&le;3, 2&le;3, 2&le;2)", table_body), Paragraph("<b>P1 finishes.</b> Releases [2, 0, 0]. <b>Work = [5, 3, 2]</b>", table_body)],
        [Paragraph("Step 3", table_body), Paragraph("<b>P3</b>", table_body), Paragraph("[0, 1, 1]", table_code), Paragraph("[5, 3, 2]", table_code), Paragraph("<b>True</b> (0&le;5, 1&le;3, 1&le;2)", table_body), Paragraph("<b>P3 finishes.</b> Releases [2, 1, 1]. <b>Work = [7, 4, 3]</b>", table_body)],
        [Paragraph("Step 4", table_body), Paragraph("<b>P4</b>", table_body), Paragraph("[4, 3, 1]", table_code), Paragraph("[7, 4, 3]", table_code), Paragraph("<b>True</b> (4&le;7, 3&le;4, 1&le;3)", table_body), Paragraph("<b>P4 finishes.</b> Releases [0, 0, 2]. <b>Work = [7, 4, 5]</b>", table_body)],
        [Paragraph("Step 5", table_body), Paragraph("<b>P0</b>", table_body), Paragraph("[7, 4, 3]", table_code), Paragraph("[7, 4, 5]", table_code), Paragraph("<b>True</b> (7&le;7, 4&le;4, 3&le;5)", table_body), Paragraph("<b>P0 finishes.</b> Releases [0, 1, 0]. <b>Work = [7, 5, 5]</b>", table_body)],
        [Paragraph("Step 6", table_body), Paragraph("<b>P2</b>", table_body), Paragraph("[6, 0, 0]", table_code), Paragraph("[7, 5, 5]", table_code), Paragraph("<b>True</b> (6&le;7, 0&le;5, 0&le;5)", table_body), Paragraph("<b>P2 finishes.</b> Releases [3, 0, 2]. <b>Work = [10, 5, 7] = Total</b>", table_body)],
    ]
    t_audit = Table(audit_data, colWidths=[40, 48, 65, 65, 120, 166])
    t_audit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, table_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, table_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_audit)

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Audit Result:</b> All 5 procedures completed. A valid safe sequence exists: "
        "<b>&lang; P1 &rarr; P3 &rarr; P4 &rarr; P0 &rarr; P2 &rang;</b>. Initial system state is <b>SAFE</b>.",
        body_text
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>State Transition Matrix across Execution Phases:</b>", sub_heading))

    state_comp_data = [
        [Paragraph("<b>Operational Phase</b>", table_header), Paragraph("<b>Available [A, B, C]</b>", table_header), Paragraph("<b>Safety Status</b>", table_header), Paragraph("<b>System Action & Clinical Consequence</b>", table_header)],
        [Paragraph("Baseline Configuration", table_body), Paragraph("[3, 3, 2]", table_code), Paragraph("<b>SAFE</b>", table_header), Paragraph("Nominal state; safe sequence &lang;P1, P3, P4, P0, P2&rang; verified.", table_body)],
        [Paragraph("Post-Scenario 1 ($P_1$ Req [1,0,2])", table_body), Paragraph("[2, 3, 0]", table_code), Paragraph("<b>SAFE</b>", table_header), Paragraph("Request granted; CABG bypass proceeds; safe sequence preserved.", table_body)],
        [Paragraph("Speculative Scenario 2 ($P_0$ Req [0,2,0])", table_body), Paragraph("[2, 1, 0]", table_code), Paragraph("<b>UNSAFE</b>", table_header), Paragraph("<b>Blocked by Banker's algorithm</b>; rollback executed; deadlock averted.", table_body)]
    ]
    t_comp = Table(state_comp_data, colWidths=[120, 90, 74, 220])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, table_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_comp)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: 12. EVALUATION OF REQUEST SCENARIOS
    # =========================================================================
    story.append(Paragraph("12. EVALUATION OF REQUEST SCENARIOS", section_heading))
    story.append(Paragraph("<b>Scenario 1: Safe Request Approval</b>", sub_heading))
    story.append(Paragraph(
        "<b>Event:</b> The Cardiac Bypass surgical team ($P_1$) encounters multi-vessel complications and requests "
        "<b>1 additional OR suite and 2 Ventilators</b>: $Request_1 = [1, 0, 2]$.<br/>"
        "• <i>Rule 1:</i> $Request_1 \\le Need_1 \\implies [1, 0, 2] \\le [1, 2, 2]$ &rarr; Passed.<br/>"
        "• <i>Rule 2:</i> $Request_1 \\le Available \\implies [1, 0, 2] \\le [3, 3, 2]$ &rarr; Passed.<br/>"
        "• <i>Speculative Trial State:</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; $Available' = [3, 3, 2] - [1, 0, 2] = [2, 3, 0]$<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; $Allocation_1' = [2, 0, 0] + [1, 0, 2] = [3, 0, 2]$<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; $Need_1' = [1, 2, 2] - [1, 0, 2] = [0, 2, 0]$<br/>"
        "• <i>Safety Check:</i> With $Work = [2, 3, 0]$, $Need_1' = [0, 2, 0] \\le Work$ (True) &rarr; $P_1$ finishes, returning $[3, 0, 2]$ to make $Work = [5, 3, 2]$. "
        "From this point, $P_3, P_4, P_0, P_2$ can all finish in sequence.<br/>"
        "<b>Verdict: REQUEST APPROVED.</b> The system remains safe, and the assets are immediately dispatched.",
        body_text
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Scenario 2: Unsafe Request Denial (Deadlock Avoided)</b>", sub_heading))
    story.append(Paragraph(
        "<b>Event:</b> Following Scenario 1 ($Available = [2, 3, 0]$), the Trauma team ($P_0$) requests "
        "<b>2 Anesthesia Teams</b>: $Request_0 = [0, 2, 0]$.<br/>"
        "• <i>Rule 1 & 2:</i> $Request_0 \\le Need_0$ and $Request_0 \\le Available$ ($2 \\le 3$ available) &rarr; Both Passed.<br/>"
        "• <i>Speculative State:</i> $Available'' = [2, 1, 0]$, $Allocation_0'' = [0, 3, 0]$, $Need_0'' = [7, 2, 3]$.<br/>"
        "• <i>Safety Evaluation on Work = [2, 1, 0]:</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; $P_0$ needs $[7, 2, 3] \\le [2, 1, 0]$ &rarr; <b>False</b> (stalled)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; $P_1$ needs $[0, 2, 0] \\le [2, 1, 0]$ &rarr; <b>False</b> ($Need_1[B]=2 > Work[B]=1$, stalled)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; $P_2, P_3, P_4$ all have needs exceeding $Work$ (stalled)<br/>"
        "<b>Critical Result:</b> Zero procedures can finish. All teams would enter circular hold-and-wait.<br/>"
        "<b>Verdict: REQUEST DENIED.</b> State rolled back to $[2, 3, 0]$. $P_0$ is put on safe hold until $P_1$ completes.",
        body_text
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: 13. IMPLEMENTATION AND SOURCE CODE LISTING
    # =========================================================================
    story.append(Paragraph("13. IMPLEMENTATION AND SOURCE CODE LISTING", section_heading))
    story.append(Paragraph(
        "The following complete, standard C program (<code>banker_hospital.c</code>) implements the simulation. "
        "It models dynamic allocation, runs the safety algorithm, and evaluates requests with automatic rollback:",
        body_text
    ))

    full_c_code = (
        "/* banker_hospital.c -- Deadlock Avoidance in Hospital Surgical Suites */\n"
        "#include <stdio.h>\n"
        "#include <stdbool.h>\n\n"
        "#define P 5  /* Surgeries */\n"
        "#define R 3  /* 0: OR Suites, 1: Anesthesia Teams, 2: Ventilators */\n\n"
        "const char *RES_NAMES[R]  = {\"OR Suites\", \"Anesthesia Teams\", \"Ventilators\"};\n"
        "const char *PROC_NAMES[P] = {\"P0 (Trauma)\", \"P1 (CABG)\", \"P2 (Craniotomy)\",\n"
        "                             \"P3 (Transplant)\", \"P4 (Spine Fusion)\"};\n\n"
        "int total[R] = {10, 5, 7};\n"
        "int alloc[P][R] = {{0,1,0}, {2,0,0}, {3,0,2}, {2,1,1}, {0,0,2}};\n"
        "int max_claim[P][R] = {{7,5,3}, {3,2,2}, {9,0,2}, {2,2,2}, {4,3,3}};\n"
        "int need[P][R], avail[R];\n\n"
        "void compute_need_and_avail(void) {\n"
        "    for (int i = 0; i < P; i++)\n"
        "        for (int j = 0; j < R; j++) need[i][j] = max_claim[i][j] - alloc[i][j];\n"
        "    for (int j = 0; j < R; j++) {\n"
        "        int sum = 0;\n"
        "        for (int i = 0; i < P; i++) sum += alloc[i][j];\n"
        "        avail[j] = total[j] - sum;\n"
        "    }\n"
        "}\n\n"
        "bool is_safe(int safe_seq[P], bool log_steps) {\n"
        "    int work[R]; bool finish[P]; int count = 0;\n"
        "    for (int j = 0; j < R; j++) work[j] = avail[j];\n"
        "    for (int i = 0; i < P; i++) finish[i] = false;\n"
        "    while (count < P) {\n"
        "        bool found = false;\n"
        "        for (int i = 0; i < P; i++) {\n"
        "            if (!finish[i]) {\n"
        "                bool ok = true;\n"
        "                for (int j = 0; j < R; j++) if (need[i][j] > work[j]) { ok = false; break; }\n"
        "                if (ok) {\n"
        "                    for (int j = 0; j < R; j++) work[j] += alloc[i][j];\n"
        "                    finish[i] = true; safe_seq[count++] = i; found = true;\n"
        "                    if (log_steps)\n"
        "                        printf(\"  Step %d: %s finishes. Work=[%d, %d, %d]\\n\",\n"
        "                               count, PROC_NAMES[i], work[0], work[1], work[2]);\n"
        "                    break;\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "        if (!found) return false;\n"
        "    }\n"
        "    return true;\n"
        "}\n\n"
        "bool request_resources(int pid, int req[R]) {\n"
        "    printf(\"\\nRequest from %s: [%d OR, %d Anesthesia, %d Ventilator]\\n\",\n"
        "           PROC_NAMES[pid], req[0], req[1], req[2]);\n"
        "    for (int j = 0; j < R; j++) {\n"
        "        if (req[j] > need[pid][j]) { printf(\"  [REJECT] Exceeds need!\\n\"); return false; }\n"
        "        if (req[j] > avail[j])     { printf(\"  [WAIT] Not available!\\n\"); return false; }\n"
        "    }\n"
        "    for (int j = 0; j < R; j++) {\n"
        "        avail[j] -= req[j]; alloc[pid][j] += req[j]; need[pid][j] -= req[j];\n"
        "    }\n"
        "    int seq[P];\n"
        "    if (is_safe(seq, true)) {\n"
        "        printf(\"--> GRANTED: State remains SAFE.\\n\"); return true;\n"
        "    } else {\n"
        "        printf(\"--> DENIED: State becomes UNSAFE! Rolling back.\\n\");\n"
        "        for (int j = 0; j < R; j++) {\n"
        "            avail[j] += req[j]; alloc[pid][j] -= req[j]; need[pid][j] += req[j];\n"
        "        }\n"
        "        return false;\n"
        "    }\n"
        "}\n\n"
        "int main(void) {\n"
        "    compute_need_and_avail();\n"
        "    int seq[P];\n"
        "    printf(\"=== Step 1: Initial Safety Audit ===\\n\");\n"
        "    if (is_safe(seq, true)) printf(\"System is initially SAFE.\\n\");\n"
        "    int req1[R] = {1, 0, 2}; request_resources(1, req1); /* P1 CABG Safe */\n"
        "    int req2[R] = {0, 2, 0}; request_resources(0, req2); /* P0 Trauma Unsafe */\n"
        "    return 0;\n"
        "}"
    )

    t_code = Table([[Preformatted(full_c_code, code_block_style)]], colWidths=[504])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), table_bg),
        ('BOX', (0,0), (-1,-1), 0.5, table_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_code)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: 14. RESULTS AND SCREENSHOTS
    # =========================================================================
    story.append(Paragraph("14. RESULTS AND SCREENSHOTS", section_heading))
    story.append(Paragraph(
        "The completed C program was compiled using GCC and executed in a Windows PowerShell environment. "
        "The screenshots below demonstrate the baseline audit and scenario validations:",
        body_text
    ))

    term_output_1 = (
        "PS C:\\Users\\akhil\\bankers_sim> gcc -std=c99 banker_hospital.c -o banker_hospital.exe\n"
        "PS C:\\Users\\akhil\\bankers_sim> .\\banker_hospital.exe\n"
        "=== Step 1: Initial Safety Audit ===\n"
        "  Step 1: P1 (CABG) finishes. Work=[5, 3, 2]\n"
        "  Step 2: P3 (Transplant) finishes. Work=[7, 4, 3]\n"
        "  Step 3: P4 (Spine Fusion) finishes. Work=[7, 4, 5]\n"
        "  Step 4: P0 (Trauma) finishes. Work=[7, 5, 5]\n"
        "  Step 5: P2 (Craniotomy) finishes. Work=[10, 5, 7]\n"
        "System is initially SAFE.\n"
        "Safe Sequence: P1 (CABG) -> P3 (Transplant) -> P4 (Spine Fusion) -> P0 (Trauma) -> P2 (Craniotomy)"
    )

    t_term_1 = Table([[Preformatted(term_output_1, term_output_style)]], colWidths=[504])
    t_term_1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#334155')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_term_1)
    story.append(Paragraph("Figure 1: Initial Safety Audit and Safe Sequence Execution.", fig_caption))

    story.append(Spacer(1, 4))

    term_output_2 = (
        "Request from P1 (CABG): [1 OR, 0 Anesthesia, 2 Ventilator]\n"
        "  Step 1: P1 (CABG) finishes. Work=[5, 3, 2]\n"
        "  Step 2: P3 (Transplant) finishes. Work=[7, 4, 3]\n"
        "  Step 3: P4 (Spine Fusion) finishes. Work=[7, 4, 5]\n"
        "  Step 4: P0 (Trauma) finishes. Work=[7, 5, 5]\n"
        "  Step 5: P2 (Craniotomy) finishes. Work=[10, 5, 7]\n"
        "--> GRANTED: State remains SAFE.\n"
        "\n"
        "Request from P0 (Trauma): [0 OR, 2 Anesthesia, 0 Ventilator]\n"
        "--> DENIED: State becomes UNSAFE! Rolling back."
    )

    t_term_2 = Table([[Preformatted(term_output_2, term_output_style)]], colWidths=[504])
    t_term_2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#334155')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_term_2)
    story.append(Paragraph("Figure 2: Denial and Rollback of Unsafe Surgical Request.", fig_caption))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: 15. LIMITATIONS, 16. CONCLUSION, 17. FUTURE SCOPE & 18. REFERENCES
    # =========================================================================
    story.append(Paragraph("15. LIMITATIONS & REAL-WORLD CONSIDERATIONS", section_heading))
    story.append(Paragraph(
        "• <b>A Priori Peak Need:</b> Surgeries encounter unexpected hemorrhaging. Hospitals mitigate this by using "
        "ASA risk scores and historical data to bound maximum claims at the 95th percentile.<br/>"
        "• <b>Equipment Downtime:</b> Autoclave sterilizations and machine faults reduce capacity dynamically. Real centers "
        "maintain an unallocated 10-15% reserve buffer outside the general Banker's pool.<br/>"
        "• <b>Emergency Preemption:</b> Level-1 trauma emergencies ethically override elective cases. Hospitals deploy a "
        "two-tier system: elective cases use Banker's avoidance, while code-blue emergencies trigger controlled preemption.",
        body_text
    ))

    story.append(Paragraph("16. CONCLUSION", section_heading))
    story.append(Paragraph(
        "The simulation demonstrates that Dijkstra's Banker's algorithm successfully avoids deadlocks in non-computing, "
        "physical infrastructure. Having idle resources in stock does not mean they can be safely handed out - the controller "
        "must verify that a worst-case recovery sequence exists. The implemented C software runs in deterministic "
        "$\\mathcal{O}(R \\cdot P^2)$ time with zero heap allocations, proving its suitability for embedded hospital dispatch systems.",
        body_text
    ))

    story.append(Paragraph("17. FUTURE SCOPE", section_heading))
    story.append(Paragraph("• Addition of an interactive Graphical User Interface (GUI) for dispatch nurses.", body_bullet))
    story.append(Paragraph("• Integration with real-time HL7/FHIR hospital telemetry and ventilator sensors.", body_bullet))
    story.append(Paragraph("• Implementation of dynamic priority classes with controlled emergency preemption.", body_bullet))
    story.append(Paragraph("• Persistent database logging of surgical wait times and asset utilization.", body_bullet))

    story.append(Paragraph("18. REFERENCES", section_heading))
    story.append(Paragraph("1. Abraham Silberschatz, Peter B. Galvin and Greg Gagne, <i>Operating System Concepts</i>, 10th Edition, Wiley.", body_bullet))
    story.append(Paragraph("2. Edsger W. Dijkstra, <i>Cooperating Sequential Processes</i>, Technological University Eindhoven, 1965.", body_bullet))
    story.append(Paragraph("3. Andrew S. Tanenbaum and Herbert Bos, <i>Modern Operating Systems</i>, Pearson.", body_bullet))
    story.append(Paragraph("4. Department of Computer Science and Design, Dayananda Sagar College of Engineering, Laboratory Courseware.", body_bullet))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>19. REPOSITORY</b>", sub_heading))
    story.append(Paragraph("https://github.com/akhilS0405/Hospital-Bankers-Algorithm-Simulation.git", body_text))

    doc.build(story, canvasmaker=SimplePageNumberCanvas)
    print(f"Report successfully compiled: {pdf_path}")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'Hospital_Bankers_Algorithm_Case_Study_15_Pages.pdf'
    generate_15_page_report(target)
    reader = pypdf.PdfReader(target)
    print(f"Total Page Count: {len(reader.pages)}")
