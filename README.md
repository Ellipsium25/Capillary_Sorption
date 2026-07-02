# Mathematical Modeling of Capillary Sorption

## Overview
This repository contains the mathematical models, numerical solvers, and experimental data for analyzing capillary sorption under trapped-air back-pressure. Originally developed during a research stint at CSIR-IMMT, the project reformulates the classical Washburn equation and utilizes Python-based ODE solvers to simulate discontinuous bubble-release dynamics in powder sorption systems.

## Core Features
* **Modified Washburn Modeling:** Translates classical length-based force balances into mass-based variables to accurately map against tensiometer data.
* **Bubble-Release Dynamics:** Utilizes an Euler-integration model to capture the logarithmic-halt and periodic-jump behavior observed in experimental mass-uptake curves.
* **Geometric Sensitivity Analysis:** Evaluates various perforation designs (hole count vs. radius) at a constant effective area to determine sorption-inhibition thresholds via critical contact angle vs. pressure phase-space diagrams.

## Repository Structure
* `sorption_model.py` / `sorption_model3.py`: Core numerical ODE solvers built with NumPy and SciPy[cite: 2].
* `trial1.py`, `trial3.py`, `trial4.py`: Experimental script files containing specific multi-variable test runs[cite: 2].
* `Physical_Phase_Space_Models.xlsx`: Datasets and phase-space diagram visualizations for the comparative geometric sensitivity analysis[cite: 2].
* `sorption_model_conclusions_initial.pdf`: Detailed research findings, mathematical derivations, and initial project conclusions[cite: 2].
* `LICENSE`: Standard project license information[cite: 2].

## Tech Stack
* **Language:** Python
* **Libraries:** NumPy, SciPy
