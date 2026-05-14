# UI/UX Design Specification: Market Pulse & Safety Features

## Overview
This document outlines the UI components and design system updates for the TradeVision AI platform. The goal is to elevate the professional feel of the tool while adding core features like market-wide pulse monitoring and safety scanning.

## 1. Visual Identity Updates
- **Typography**: Shifted to a bolder, more authoritative scale (900/800 weights for headers).
- **Color Palette**:
  - Indigo-600: Primary Action / Brand
  - Emerald-500: Success / Safe / Positive Trend
  - Rose-500: High Risk / Negative Trend
  - Slate-900: Deep Contrast for core panels
- **Layout**: Increased border-radius (up to 40px/3xl) for a modern, "glassmorphism-light" feel. Increased padding (p-8/p-10) for clarity.

## 2. Landing Page Components
### A. Market Pulse Header
- **Location**: Sticky top navigation.
- **Data Points**: SPY, QQQ, DIA.
- **Function**: Provide immediate market context (Current Price + 24h Change %) so the user knows the "macro climate" before searching a specific ticker.

### B. Control Bar (Toggles)
- **Location**: Above the central search bar.
- **Features**:
  - **Risk Profile**: [Standard | Conservative]. This will eventually hook into the scoring engine to weight fundamentals (Conservative) vs. technicals/momentum (Standard).
  - **Time Horizon**: [Day | Short | Long]. Changes the context of the technical indicator interpretation (e.g., Short = 50-day focus, Long = 200-day focus).

### C. Safety Scanner Section
- **Location**: Below the fold (Hero section).
- **Content**: 3 spotlight cards showing "Top Movers" or "Popular Searches" with a Safety Badge (Very Safe, High Risk, Growth Star).
- **Purpose**: Drive engagement and show the power of the "Scanner" logic before a user even enters a ticker.

## 3. Report Page (V2)
- **Signal Badge**: Transformed into a large, high-confidence "card" with a progress bar for Confidence Score.
- **Safety Card**: Integrated into the left panel. Shows "Volatility Risk" and "Institutional Safety" meters.
- **Data Hierarchy**: Technicals and Fundamentals are now split into clean, card-based grids with institutional holders highlighted in a distinct sub-panel.

## 4. Implementation Notes for Software Engineer
- **Framework**: Tailwind CSS.
- **Responsive**: All cards use `md:grid-cols-X` and `lg:grid-cols-Y` for mobile-first responsiveness.
- **Templates**:
  - `landing_page_redesign.html` -> Use for `index.html` structure.
  - `report_template_v2.html` -> Use for `report_template.html` structure.
- **Dynamic Data**: Ticker, Company Name, Price, Change, Signal, Confidence, Technicals list, Fundamentals (PE, Growth, Margin), Holders list, Thesis text, and Timestamp.

---
**Artifacts**: 
- `/home/team/shared/landing_page_redesign.html`
- `/home/team/shared/report_template_v2.html`
