# Lab-1-Project
# Building a Profile HMM for the Kunitz-Type Protease Inhibitor Domain (PF00014)

This repository contains a complete pipeline to build and validate a **Profile Hidden Markov Model (HMM)** for the **Kunitz-type protease inhibitor domain** (Pfam: **PF00014**). The final model is designed for sensitive domain detection in large protein datasets.

## Project Goal
- Build a Profile HMM trained on **structurally aligned** Kunitz domains.
- Validate the model on **independent UniProt-derived** positive/negative test sets.
- Select an optimal E-value threshold and report performance using **confusion matrix** metrics, with **MCC** as the main comparison metric.

## Background
The **Kunitz domain** is a protease inhibitor domain found across many species and proteins (e.g., BPTI/Aprotinin as the classic reference). This project focuses on detecting PF00014 occurrences reliably in protein sequences.

## Methods Overview

### 1) Training Data Collection (PDB → FASTA)
- Download a customized list of PDB structures related to PF00014.
- Filter criteria:
  - **Resolution ≤ 2.5 Å**
  - **Pfam family PF00014**
  - **Sequence length ~45–80 aa**
- Convert to FASTA, removing non-PF00014 chains when multiple Pfam IDs exist.

### 2) Redundancy Reduction (CD-HIT)
- Cluster sequences with **CD-HIT** at default **0.9 identity threshold** to reduce bias from redundant structures.
- Inspect problematic entries (e.g., overly long chains) and remove if poorly aligned.

### 3) Structural Multiple Sequence Alignment (PDB-e Fold)
- Run structural alignment with **PDB-e Fold**.
- Remove abnormal sequences (e.g., very short chains) from the alignment.
- Export alignment in FASTA format.

### 4) Build the Profile HMM (HMMER)
- Build model using `hmmbuild` (HMMER).
- Visualize the model logo using **Skylign**.

### 5) Independent Validation (UniProt + BLAST filtering)
- Download independent UniProt-derived datasets:
  - Positives: Kunitz-containing sequences
  - Negatives: non-Kunitz sequences
- Remove overlaps with training data using BLAST:
  - Exclude entries with **>95% sequence identity** and **>50 aligned residues** vs training sequences.
- Split into two sets (set_1 / set_2), run `hmmsearch`, and evaluate multiple thresholds.
- Choose **E-value threshold = 1e-6** as the best trade-off.

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
- D3GGZ8 (E=0.0096)
- A0A1Q1NL17 (E=0.00016)
- Q8WPG5 (E=0.00025)
- O62247 (E=9.5e-05)

## How to Reproduce (High-level)
> Adjust file names/paths to match your repo structure.

1. **Prepare training FASTA**
   - Download & filter PDB PF00014 entries
   - Convert to FASTA (PF00014-only chains)

2. **Cluster to remove redundancy**
   ```bash
   cd-hit -i kunitz_raw.fasta -o kunitz_cdhit.fasta -c 0.9
