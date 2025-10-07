This document demonstrates how to use AI as a code reviewer for learning and development purposes. This is a companion to Chapter 2, Video 9 "Coding Project - Review Python code with AI".

## Overview

Learn to leverage AI for constructive code reviews by providing clear roles, context, and specific formatting requirements. This approach helps simulate real-world code review experiences.

### The Prompt

Copy and use this exact prompt with your AI assistant when reviewing code:

```
Role: Staff Engineer & code reviewer — kind but direct.

Context: The class below was written by a new grad for a tiny in-memory Books service.

Task: Critique the class with a prioritized list. Use tags [Blocker], [Major], [Minor]. For each item include:
1) the issue, 2) why it matters, 3) the smallest fix (code or one-line diff).

Keep it under 12 bullets. Suggest only minimal changes that keep the spirit of the code.
```
