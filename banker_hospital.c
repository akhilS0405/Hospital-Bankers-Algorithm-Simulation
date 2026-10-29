/*
 * ============================================================================
 * College    : DAYANANDA SAGAR COLLEGE OF ENGINEERING
 * Department : Department of Computer Science and Design (CSD)
 * Course     : Operating Systems (3rd Semester / CG)
 * Academic Yr: 2026–2027
 * Student    : AKHIL SRINATH (USN: 1DS25CG003)
 * Faculty    : Prof. NAYANA SHINDE
 * Assignment : #5 - Real-Life Application of Banker's Algorithm Case Study
 * Domain     : Smart Hospital Operating Room & ICU Resource Allocation
 * File       : banker_hospital.c
 * ============================================================================
 */

#include <stdio.h>
#include <stdbool.h>

#define P 5  /* Number of surgical procedures (Processes) */
#define R 3  /* Number of critical resource types */

/* Resource and procedure labels */
const char *RES_NAMES[R] = {
    "Operating Rooms",
    "Anesthesia Teams",
    "Ventilators"
};

const char *PROC_NAMES[P] = {
    "P0 (Trauma Laparotomy)",
    "P1 (Cardiac Bypass - CABG)",
    "P2 (Pediatric Craniotomy)",
    "P3 (Liver/Kidney Transplant)",
    "P4 (Spine Fusion)"
};

/* Total physical resources in hospital inventory: E = [10, 5, 7] */
int total[R] = {10, 5, 7};

/* Currently allocated resources for each procedure */
int alloc[P][R] = {
    {0, 1, 0},  /* P0 */
    {2, 0, 0},  /* P1 */
    {3, 0, 2},  /* P2 */
    {2, 1, 1},  /* P3 */
    {0, 0, 2}   /* P4 */
};

/* Declared maximum resource claims */
int max_claim[P][R] = {
    {7, 5, 3},  /* P0 */
    {3, 2, 2},  /* P1 */
    {9, 0, 2},  /* P2 */
    {2, 2, 2},  /* P3 */
    {4, 3, 3}   /* P4 */
};

int need[P][R];
int avail[R];

void compute_need(void) {
    for (int i = 0; i < P; i++) {
        for (int j = 0; j < R; j++) {
            need[i][j] = max_claim[i][j] - alloc[i][j];
        }
    }
}

void compute_available(void) {
    for (int j = 0; j < R; j++) {
        int sum = 0;
        for (int i = 0; i < P; i++) {
            sum += alloc[i][j];
        }
        avail[j] = total[j] - sum;
    }
}

void print_state(void) {
    printf("\n%-28s | %-12s | %-12s | %-12s\n", "Procedure", "Allocation", "Max Claim", "Need");
    printf("-----------------------------+--------------+--------------+--------------\n");
    for (int i = 0; i < P; i++) {
        printf("%-28s | [%d, %d, %d]    | [%d, %d, %d]    | [%d, %d, %d]\n",
               PROC_NAMES[i],
               alloc[i][0], alloc[i][1], alloc[i][2],
               max_claim[i][0], max_claim[i][1], max_claim[i][2],
               need[i][0], need[i][1], need[i][2]);
    }
    printf("-----------------------------+--------------+--------------+--------------\n");
    printf("Available Resources: [%d ORs, %d Anesthesia Teams, %d Ventilators]\n\n",
           avail[0], avail[1], avail[2]);
}

bool is_safe(int safe_seq[P], bool log_steps) {
    int work[R];
    bool finish[P];
    int count = 0;

    for (int j = 0; j < R; j++) {
        work[j] = avail[j];
    }
    for (int i = 0; i < P; i++) {
        finish[i] = false;
    }

    while (count < P) {
        bool found = false;

        for (int i = 0; i < P; i++) {
            if (!finish[i]) {
                bool can_run = true;
                for (int j = 0; j < R; j++) {
                    if (need[i][j] > work[j]) {
                        can_run = false;
                        break;
                    }
                }

                if (can_run) {
                    for (int j = 0; j < R; j++) {
                        work[j] += alloc[i][j];
                    }
                    finish[i] = true;
                    safe_seq[count++] = i;
                    found = true;

                    if (log_steps) {
                        printf("  Step %d: %s finishes. Work=[%d, %d, %d]\n",
                               count, PROC_NAMES[i], work[0], work[1], work[2]);
                    }
                    break;
                }
            }
        }

        if (!found) {
            return false;
        }
    }
    return true;
}

bool request_resources(int pid, int req[R]) {
    printf("------------------------------------------------------------------------\n");
    printf("Request from %s: [%d ORs, %d Anesthesia, %d Ventilators]\n",
           PROC_NAMES[pid], req[0], req[1], req[2]);
    printf("------------------------------------------------------------------------\n");

    /* Rule 1: Request <= Need */
    for (int j = 0; j < R; j++) {
        if (req[j] > need[pid][j]) {
            printf("Error: Request exceeds declared maximum need for %s!\n\n", RES_NAMES[j]);
            return false;
        }
    }

    /* Rule 2: Request <= Available */
    for (int j = 0; j < R; j++) {
        if (req[j] > avail[j]) {
            printf("Notice: Insufficient %s available. %s must wait.\n\n",
                   RES_NAMES[j], PROC_NAMES[pid]);
            return false;
        }
    }

    /* Rule 3: Speculative trial allocation */
    for (int j = 0; j < R; j++) {
        avail[j] -= req[j];
        alloc[pid][j] += req[j];
        need[pid][j] -= req[j];
    }

    int test_seq[P];
    if (is_safe(test_seq, true)) {
        printf("--> Request GRANTED: State remains safe.\n");
        printf("    Safe Sequence: ");
        for (int i = 0; i < P; i++) {
            printf("%s%s", PROC_NAMES[test_seq[i]], (i == P - 1) ? "\n\n" : " -> ");
        }
        print_state();
        return true;
    } else {
        printf("--> Request DENIED: State becomes unsafe (deadlock possible)!\n");
        printf("    Rolling back changes. %s must wait for resources to free up.\n\n",
               PROC_NAMES[pid]);

        /* Rollback */
        for (int j = 0; j < R; j++) {
            avail[j] += req[j];
            alloc[pid][j] -= req[j];
            need[pid][j] += req[j];
        }
        return false;
    }
}

int main(void) {
    printf("========================================================================\n");
    printf("    HOSPITAL SURGICAL DISPATCHER - BANKER'S ALGORITHM SIMULATION        \n");
    printf("========================================================================\n");

    compute_need();
    compute_available();
    print_state();

    /* Step 1: Initial Safety Audit */
    int seq[P];
    printf(">>> Step 1: Initial System Safety Audit\n");
    if (is_safe(seq, true)) {
        printf("System is initially SAFE.\nSafe Sequence: ");
        for (int i = 0; i < P; i++) {
            printf("%s%s", PROC_NAMES[seq[i]], (i == P - 1) ? "\n\n" : " -> ");
        }
    } else {
        printf("System is initially UNSAFE!\n");
        return 1;
    }

    /* Step 2: Safe request - P1 requests [1, 0, 2] */
    printf(">>> Step 2: Scenario 1 - P1 (Cardiac Bypass) requests [1, 0, 2]\n");
    int req1[R] = {1, 0, 2};
    request_resources(1, req1);

    /* Step 3: Unsafe request - P0 requests [0, 2, 0] */
    printf(">>> Step 3: Scenario 2 - P0 (Trauma) requests [0, 2, 0]\n");
    int req2[R] = {0, 2, 0};
    request_resources(0, req2);

    return 0;
}
