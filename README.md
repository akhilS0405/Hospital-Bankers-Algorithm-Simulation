# Real-Life Application of Banker's Algorithm
### Operating Systems Mini Project / Case Study Report
**Department of Computer Science and Design | Dayananda Sagar College of Engineering**

* **Student:** Akhil Srinath
* **USN:** 1DS25CG003
* **Class / Section:** 3rd Sem / CG
* **Course:** CS304 - Operating Systems
* **Faculty Guide:** Prof. Nayana Shinde
* **Academic Year:** 2026–2027

---

## 📌 Project Overview
This project presents an educational simulation of **Dijkstra's Banker's Algorithm** applied to a real-life cyber-physical domain: a **Smart Hospital Surgical Suite and Intensive Care Unit (ICU)**.

Five concurrent surgical procedures compete for three scarce clinical assets:
1. **Resource A (OR Suites):** 10 units
2. **Resource B (Anesthesia Teams):** 5 units
3. **Resource C (Ventilators):** 7 units

The simulation verifies the safety of the baseline configuration, prints the safe execution sequence, and dynamically tests resource requests—approving safe expansions and denying/rolling back unsafe requests to prevent circular deadlocks.

---

## 📁 Repository Structure
```
├── banker_hospital.c                                # Main ANSI C simulation source code
├── Hospital_Bankers_Algorithm_Case_Study_15_Pages.pdf # 15-Page formal academic report
├── Hospital_Bankers_Algorithm_Case_Study.pdf          # Mirror of the formal report
├── build_15_page_report.py                          # ReportLab automated PDF generator
└── README.md                                        # Documentation and build instructions
```

---

## 🚀 Compilation & Execution

To compile and run the simulation using GCC or Clang:

```bash
# Compilation (C99 Standard)
gcc -std=c99 -Wall -Wextra banker_hospital.c -o banker_hospital

# Execution on Windows
.\banker_hospital.exe

# Execution on Linux / macOS
./banker_hospital
```

---

## 📊 Sample Execution Output

```
========================================================================
    HOSPITAL SURGICAL DISPATCHER - BANKER'S ALGORITHM SIMULATION        
========================================================================

Procedure                    | Allocation   | Max Claim    | Need        
-----------------------------+--------------+--------------+--------------
P0 (Trauma Laparotomy)       | [0, 1, 0]    | [7, 5, 3]    | [7, 4, 3]
P1 (Cardiac Bypass - CABG)   | [2, 0, 0]    | [3, 2, 2]    | [1, 2, 2]
P2 (Pediatric Craniotomy)    | [3, 0, 2]    | [9, 0, 2]    | [6, 0, 0]
P3 (Liver/Kidney Transplant) | [2, 1, 1]    | [2, 2, 2]    | [0, 1, 1]
P4 (Spine Fusion)            | [0, 0, 2]    | [4, 3, 3]    | [4, 3, 1]
-----------------------------+--------------+--------------+--------------
Available Resources: [3 ORs, 3 Anesthesia Teams, 2 Ventilators]

>>> Step 1: Initial System Safety Audit
System is initially SAFE.
Safe Sequence: P1 (Cardiac Bypass - CABG) -> P3 (Liver/Kidney Transplant) -> P4 (Spine Fusion) -> P0 (Trauma Laparotomy) -> P2 (Pediatric Craniotomy)

>>> Step 2: Scenario 1 - P1 (Cardiac Bypass) requests [1, 0, 2]
--> Request GRANTED: State remains safe.

>>> Step 3: Scenario 2 - P0 (Trauma) requests [0, 2, 0]
--> Request DENIED: State becomes unsafe (deadlock possible)!
    Rolling back changes. P0 (Trauma Laparotomy) must wait for resources to free up.
```
