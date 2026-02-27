# Research Intelligence Agents

This file defines all AI agents used in the ResearchFlash system.

---

## 1. Research Summary Agent

### Purpose
Reads financial research reports and produces structured summaries.

### Input
- Raw research report text (PDF extracted)
- Up to 120,000 characters

### Output Structure
1. Core Viewpoints
2. Earnings & Key Financial Data
3. Investment Logic Breakdown
4. Risk Factors
5. 300-word Executive Summary
6. Compliance Disclaimer

### Constraints
- Must not provide investment advice
- Must not predict stock price
- Must not fabricate data
- Must remain neutral

### Model
Recommended:
- gpt-4o-mini (cost-efficient)
- gpt-4.1 for higher accuracy

Temperature:
0.2

---

## 2. Chunking Agent (Optional for Long Reports)

### Purpose
Handles long documents exceeding model context window.

### Process
1. Split document into chunks
2. Summarize each chunk
3. Merge chunk summaries
4. Send merged result to Research Summary Agent

### Chunk Size
3,000–5,000 words

---

## 3. Compliance Guard Agent

### Purpose
Ensures output does not violate financial advisory regulations.

### Responsibilities
- Remove buy/sell language
- Remove price target recommendations
- Remove guaranteed returns
- Append disclaimer

---

## Data Flow

PDF → Text Extraction → Chunking Agent (if needed)
→ Research Summary Agent → Compliance Guard Agent
→ Final Output

---

## Future Expandable Agents

- Sentiment Analysis Agent
- Financial Anomaly Detection Agent
- Multi-Report Comparison Agent
- Earnings Call Transcript Agent
- Portfolio Insight Agent

---

End of agents configuration.