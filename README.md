# Lab-1-Project
# Building a Profile HMM for the Kunitz-Type Protease Inhibitor Domain (PF00014)

## In this Project
- A Profile Hidden Markov Model for the Kunitz domain is built.
- Model is tested with **independent UniProt-derived** positive/negative test sets.
- With cross-validation ptimal E-value threshold is selected and performance is reported using **confusion matrix** metrics, with **MCC** as the main comparison metric.

## Background
The **Kunitz domain** is a protease inhibitor domain found across many species and proteins. This project focuses on detecting PF00014 occurrences reliably in protein sequences.

## Methods Overview

### 1) Training Data Collection
- A customized list of PDB structures related to PF00014 is downloaded.
- Filter criteria:
  - **Resolution ≤ 2.5 Å**
  - **Pfam family PF00014**
  - **Sequence length ~45–80 aa**
- Converted to FASTA, non-PF00014 chains are removed when multiple Pfam IDs exist.

### 2) Redundancy Reduction (CD-HIT)
- Sequences are clustered with **CD-HIT** at default **0.9 identity threshold** to reduce bias from redundant structures.
- 20DY_E is removed from the dataset (long and poorly aligned).

### 3) Multiple Sequence Alignment (PDB-e Fold)
- Multiple sequence alignment with **PDB-e Fold** is obtained.
- 5JBT is removed from the dataset and the alignment (very short).
- Export alignment in FASTA format.

### 4) Build the Profile HMM (HMMER)
- Model is built using `hmmbuild` (HMMER).
- Model logo is visualized using **Skylign**.

### 5) Model Testing (UniProt + BLAST filtering)
- UniProt-derived datasets are downloaded:
  - Positives: Kunitz-containing sequences
  - Negatives: non-Kunitz sequences
- Overlaps with training data are removed using BLAST:
  - Entries with **>95% sequence identity** and **>50 aligned residues** vs training sequences is determined with BLAST then removed.
- Split into two sets (set_1 / set_2), run `hmmsearch`, and evaluate multiple thresholds.
- Choose **E-value threshold = 1e-6** as it was the best trade-off.

## Results (Threshold = 1e-6)

**Combined evaluation:**
- **Q2 (Accuracy): 0.999993**
- **MCC: 0.9945**
- **TPR (Recall): 0.9891**  *(364/368 positives detected; FN=4)*
- **PPV (Precision): 1.0**   *(FP=0)*

**Confusion Matrix counts:**
- **TN = 572,832**
- **TP = 364**
- **FN = 4**
- **FP = 0**

### False Negatives
Four known Kunitz-containing proteins were missed because their **full-sequence E-values** were above the 1e-6 threshold:
- D3GGZ8
- A0A1Q1NL17
- Q8WPG5
- O62247 
