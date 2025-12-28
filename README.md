# Enterprise Social Media Orchestrator (65k Scale)

A high-performance, asynchronous web scraping system built for large-scale data extraction across Instagram, TikTok, and LinkedIn.

## 🚀 Key Features

- **Asynchronous Orchestration:** Utilizes `asyncio.Queue` to manage 65,000+ targets with optimized concurrency control.
- **Browser Automation:** Powered by **Playwright** to navigate JavaScript-heavy environments and infinite scrolling.
- **Anti-Bot Mitigation:** Integrates **Residential Proxy Rotation** and custom header fingerprinting to bypass IP rate limits.
- **Data Pipeline:** Automated cleaning and storage using **Pandas**, exporting to validated CSV/JSON formats.

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Automation:** Playwright (Chromium)
- **Concurrency:** Asyncio
- **Proxy Management:** Custom Proxy Rotation Logic
- **Data Handling:** Pandas

## 📈 Scalability Note

This project is designed to be deployed as an **Apify Actor**. By separating the scraper logic from the orchestrator, the system can be horizontally scaled across multiple server instances to handle millions of requests monthly.

## ⚙️ Setup

1. `pip install playwright pandas`
2. `playwright install chromium`
3. Configure `proxy_handler.py` with your credentials.
4. Run `python orchestrator.py`.
