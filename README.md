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

# 🚀 Step-by-Step Setup Guide

## 1️⃣ Prerequisites & Secrets

- Clone or fork this repository
- Create a Slack Incoming Webhook URL
- Generate a Google Gemini API Key

---

## 2️⃣ Setup Jenkins using Docker

Run Jenkins container:

```bash
docker run -d \
  -p 8080:8080 \
  -p 50000:50000 \
  --name jenkins-ai \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

# Access the container as root to install Python natively

docker exec -u root -it jenkins-ai bash
apt-get update && apt-get install -y python3 python3-venv python3-pip
exit

## 🔐 Retrieve Jenkins Admin Password

docker exec jenkins-ai cat /var/jenkins_home/secrets/initialAdminPassword

--------------------------------------------------

## ⚙️ Pipeline Configuration

### 🔑 Inject Credentials

In Jenkins, navigate to:

Manage Jenkins → Credentials → System → Global credentials

Add:

- Secret Text
  ID: llm-api-key (Gemini API Key)

- Secret Text
  ID: slack-webhook-url (Slack Webhook URL)

--------------------------------------------------

### ✅ Approve Groovy Sandbox Methods

Go to:

Manage Jenkins → In-Process Script Approval

Approve the following signatures:

- getRawBuild
- getLog

--------------------------------------------------

### 🛠️ Create the Job

1. Create a new Pipeline item
2. Select Pipeline script from SCM
3. Choose Git
4. Enter your repository URL
5. Set branch to main
6. Set Script Path to jenkins/Jenkinsfile

--------------------------------------------------

### ▶️ Trigger the Pipeline

- Click Build Now
- Observe the pipeline:
  - Detects failure
  - Extracts logs
  - Runs Python analysis
  - Sends AI-generated summary to Slack
## 🔮 Future Enhancements

- **Jira / Linear Integration**
  Automatically create a bug ticket with the AI-generated summary when a build fails (especially on `main` or production branches).

- **Smart Log Chunking**
  Implement a chunking mechanism to process large logs without exceeding LLM token limits.

- **Advanced Failure Classification**
  Categorize failures (e.g., build error, test failure, infra issue) for better triaging and analytics.

- **Multi-Model Support**
  Add support for multiple LLM providers (OpenAI, Anthropic) with fallback mechanisms.

- **Cost Optimization Layer**
  Dynamically choose between fast/cheap vs powerful models based on log complexity.

- **Historical Insights Dashboard**
  Store past failures and visualize trends (MTTR, common errors, flaky tests).

- **Auto-Fix Suggestions (Experimental)**
  Generate and optionally trigger automated fixes (e.g., retry jobs, restart services).

- **Native Jenkins Plugin**
  Convert the Python-based system into a native Jenkins plugin for easier enterprise adoption.

- **Role-Based Notifications**
  Send alerts to specific teams based on failure type (e.g., backend, DevOps, QA).

- **Slack Interactive Actions**
  Add buttons in Slack messages (e.g., "Retry Build", "View Logs", "Create Ticket").
```
