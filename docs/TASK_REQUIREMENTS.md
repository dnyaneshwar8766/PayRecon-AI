# Onelab AI Fitness Assessment — task requirements extracted from the assignment screenshot

## Problem
A payments company knows every transaction its platform processed and knows what the bank says actually arrived. Those two records should match at month end, but they do not. The solution must find why and show where the gaps are.

## Required behavior and scenarios
- Generate your own test data; no files are supplied.
- Model the platform recording a transaction immediately and the bank batching/settling funds 1–2 days later.
- Detect a transaction settling in the following month.
- Detect rounding drift that becomes material when small per-transaction differences are summed. The sample includes two small differences that accumulate.
- Detect a duplicate entry in one dataset.
- Detect a refund with no matching original transaction.
- State assumptions. The assessment explicitly allows different assumptions if they are named.

## Required submission items (as shown)
1. Brainstorming thread: full LLM conversation; do not clean it up.
2. Distilled prompt and raw prompt: the single prompt fed into Claude Code, Cursor, or another AI coding tool.
3. Claude Code thread: full execution thread, including wrong turns.
4. Test cases written to verify the solution.
5. Working output: deployed link + code ZIP + demo video + three sentences describing what could go wrong in production.

## Important constraint
The screenshot also states that there is no single right answer, so assumptions and reasoning must be made explicit.
