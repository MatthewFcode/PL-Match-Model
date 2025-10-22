---
name: "Premier League Prediction Workflow"
description: "Defines the end-to-end flow from ML model to client queries"
ai_prompt: |
  You are an AI architect helping design an end-to-end data and model serving workflow.
  Analyze the described architecture, point out potential bottlenecks, and suggest
  improvements for scalability and performance.
---

# ⚙️ Project Flow Instructions

## 🧭 Overview
This document outlines the overall flow of the **Premier League Prediction Project**.  
It serves as both documentation and AI-readable instructions for the architecture.

## 🎯 Goal
The goal is to have **machine learning models** accurately predicting the **next 5 matches** for each Premier League team.

## 🔗 Architecture Flow

1. **Model Layer (Python / Flask)**
   - Machine learning models generate predictions for upcoming matches.
   - Served through **Flask API endpoints** (e.g. `/predict/team/<team_name>`).

2. **Backend Layer (Node.js / Express)**
   - Flask API outputs are consumed via **Express routes** in the Node.js backend.
   - This backend acts as the central data handler — fetching, validating, and passing responses through.

3. **Server Layer**
   - The Express server manages the API routes and data flow between Flask and the client.
   - Ensures reliable, asynchronous communication between Python (ML) and Node (logic).

4. **Client Layer (Frontend)**
   - The client consumes the endpoints and performs **queries** and **mutations** (e.g. fetching predictions or updating match data).
   - Displays real-time match predictions to the user.

## 🔁 Chained API Flow Summary

```text
ML Model (Flask)
   ↓
Express Routes (Node.js)
   ↓
Server (API Layer)
   ↓
Client (Queries & Mutations)

