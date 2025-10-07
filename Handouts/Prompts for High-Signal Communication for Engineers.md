# Prompts for High-Signal Communication for Engineers

---

## Slack update to an engineer teammate

**Intent:** Unblock a tiny product decision  
**Audience:** Peer engineer  
**Medium:** Slack

**Message:**
- **Status:** Fix ready behind a flag; added title validation
- **Impact:** Empty items confuse lists and generate support pings
- **Details:**
  - PR #123 adds trim + empty-check
  - Proposed UX: Block save with inline error “Title can’t be empty.”
  - Alt: auto-fill “Untitled” (not preferred)

**Ask:** Pick block vs. auto-fill by 2 p.m. so I can merge.

---

**AI prompt 1:**  
“Rewrite this for Slack using Status, Impact, Details, and end with the Ask plus the deadline.”

**AI prompt 2:**  
“Turn this into a 30-second standup update using Status, Impact, Details, then the Ask.”

---

## Prompt for Summarizing Meeting Prep Documents

Summarize the design doc for pre-meeting prep in eight or less bullets:
- Purpose 
- Decisions requested
- Key constraints (dates, SLAs, versions, or owners)
- Proposed approach 
- Top risks and mitigations
- Open questions (with suggested owner)
- Metrics and success criteria
- Links and PRs

Additionally, you can also use a prompt like the following to generate questions to ask during the meeting:  
Read the doc below and propose six meeting questions, labeled:  
1) Clarifying  
2) Scope  
3) Risk  
4) Dependency  
5) Metrics  
6) Timeline  
Keep each to one sentence. 
