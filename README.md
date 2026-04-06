# News-Driven Risk Analytics Dashboard

**Live Demo:** [https://news-driven-risk-analytics-dashboard-n6dcqgjm7bymvzwzqnbq6c.streamlit.app/]

---

## Overview

A real-time financial news analytics system that uses natural language processing (NLP) and data visualization to evaluate how media sentiment influences market risk.

The system automates the complete pipeline:

* News ingestion
* Sentiment analysis
* Dashboard visualization

---

## Problem

General-purpose sentiment models (trained on social media or reviews) are not well-suited for financial news because:

* The language is often neutral or technical
* Market-specific terms (IPO, funding, valuation) lack emotional cues
* Headlines are typically factual rather than expressive

As a result, these models frequently misclassify positive financial news as negative.

---

## Solution

This project uses a finance-specific sentiment model such as FinBERT, which is trained on financial text and analyst reports.

This improves accuracy by correctly interpreting domain-specific language.

Example:

* “Meesho’s $606M IPO pops as enthusiasm rises” → Positive

---

## Features

* Real-time news ingestion
* Finance-specific sentiment analysis
* Risk insights through dashboards
* End-to-end automated pipeline

---

## Tech Stack

* Python
* NLP (FinBERT)
* Data processing and visualization

---

## Use Cases

* Risk monitoring
* Market sentiment tracking
* Financial analytics dashboards

---

## Setup

```bash
pip install -r requirements.txt
python main.py
```
