# 🤖 AIOps CI/CD Assistant: LLM-Powered Jenkins Log Analyzer

[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-blue?logo=jenkins)](https://www.jenkins.io/)
[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Gemini API](https://img.shields.io/badge/AI-Gemini_2.5_Flash-orange)](https://deepmind.google/technologies/gemini/)
[![Slack Webhooks](https://img.shields.io/badge/Notifications-Slack-green?logo=slack)](https://slack.com/)

## 🚀 Overview

In modern CI/CD pipelines, developers often spend hours digging through thousands of lines of Jenkins console logs to find the root cause of a broken build.

This project is an **AIOps (Artificial Intelligence for IT Operations) integration** that completely automates this debugging process. By integrating Google's Gemini LLM directly into a Jenkins declarative pipeline, this tool automatically detects build failures, extracts the relevant log segments, performs intelligent root-cause analysis, and pushes a human-readable summary and actionable fix directly to a developer's Slack channel.

**Business Value:** Significantly reduces Mean Time To Recovery (MTTR) and reclaims lost developer productivity by eliminating manual log parsing.

## ✨ Key Features

- **Automated Log Extraction:** A Groovy-based pipeline script safely extracts the tail-end of failed build logs directly from the Jenkins JVM without needing complex REST API authentication.
- **LLM Integration via Prompt Engineering:** Uses Python to feed sanitized logs to the Gemini API with strict system prompts, forcing the AI to ignore "noise" and output concise, 2-step actionable solutions.
- **Real-time Slack Notifications:** Pushes nicely formatted Markdown alerts directly to the engineering team's Slack channel the second a build breaks.
- **Ephemeral Environments:** Utilizes Python `venv` within the Jenkins agent to ensure dependencies are installed and destroyed dynamically, keeping the build agent clean.

## 🏗️ High-Level System Architecture

The workflow is entirely event-driven, triggered by a `post { failure }` condition in the Jenkinsfile.

1. **Failure Detection:** Jenkins pipeline execution fails.
2. **Log Extraction:** Groovy script extracts the last 150 lines of the console log.
3. **Environment Provisioning:** Jenkins spawns an ephemeral Python virtual environment (`venv`).
4. **Log Parsing:** Python script reads and sanitizes the extracted log file.
5. **AI Analysis:** The log is sent to the Gemini API alongside a customized DevOps prompt.
6. **Notification Delivery:** The AI's root-cause analysis and fix recommendations are pushed to a Slack Webhook.

## 💻 Tech Stack

- **CI/CD Orchestration:** Jenkins (Declarative Pipelines, Groovy)
- **Scripting & API Logic:** Python 3 (Requests, OS, JSON)
- **Artificial Intelligence:** Google Gemini API (2.5 Flash Model)
- **Alerting:** Slack Incoming Webhooks
- **Infrastructure:** Docker (Jenkins LTS)

---

## 📂 Project Structure

```text
.
├── jenkins/
│   └── Jenkinsfile         # Declarative pipeline automating the CI/CD flow
├── src/
│   ├── __init__.py
│   ├── log_parser.py       # Validates, sanitizes, and extracts Jenkins logs
│   ├── llm_client.py       # Handles Prompt Engineering & Gemini API communication
│   ├── slack_notifier.py   # Formats the AI response and triggers the Slack Webhook
│   └── main.py             # Main orchestrator script executed by Jenkins
├── requirements.txt        # Python dependencies (requests)
└── README.md               # Project documentation
```
