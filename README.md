# 📚 Study-Time Optimizer

### An Intelligent Decision Support System using Linear Programming and XGBoost

A hybrid decision-support web application that helps students optimize their daily study-time allocation across multiple subjects.

The system combines:

- 📊 **Study Priority Index (SPI)** for subject prioritization
- 📐 **Linear Programming using PuLP** for optimal study-time allocation
- 🤖 **XGBoost** for experimental academic performance prediction
- 🌐 **Flask** for the web application
- 📈 **Interactive dashboard and charts** for result visualization

---

## 🚀 Project Overview

Students often struggle to decide how to distribute limited study time among multiple subjects.

A simple equal distribution of time may not be effective because subjects can differ in:

- Difficulty
- Importance
- Current performance level
- Minimum required study time
- Maximum practical study time

This project provides a data-driven approach to study planning.

The system calculates a **Study Priority Index (SPI)** for each subject, uses **Linear Programming** to determine an optimal allocation of available study hours, and then uses an **experimental XGBoost model** to estimate academic performance based on the optimized allocation.

---

## ✨ Key Features

### 📊 1. Study Priority Index (SPI)

Each subject receives a priority score based on:

- Subject Difficulty
- Subject Importance
- Current Student Performance

The system calculates:

```text
Performance Gap = 6 − Current Performance