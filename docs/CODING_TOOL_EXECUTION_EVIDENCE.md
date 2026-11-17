# AI coding-tool execution evidence

> **Do not submit this file as a Claude Code transcript.** This project was created and verified in this ChatGPT-assisted working environment; it was not executed in the user's Claude Code account. The assignment asks for the actual full coding-tool thread, including wrong turns. Export that thread from the tool you actually use and place it here. Never fabricate prompts, tool messages, errors, or debugging turns.

## Actual implementation/verification log available from this project
- Implemented a React + TypeScript + Vite dashboard and Python FastAPI backend.
- Implemented deterministic matching and discrepancy classification for late settlement, rounding difference, duplicate bank entry, unmatched refund, and additional review conditions.
- Added synthetic CSV datasets and API sample-data generation.
- Added SQLite persistence for completed reconciliation run summaries/results and history endpoints.
- Added automated tests for required scenarios and additional validation/matching cases.
- Backend test suite last verified in the build environment: 8 tests passed.
- Python compilation and ZIP archive integrity were verified.
- Frontend production build was **not** verified because dependency installation timed out in the build environment. Run `npm install` and `npm run build` locally before claiming a successful frontend build.

## Attach the real transcript
1. Open the AI coding tool used for implementation (Claude Code, Cursor, etc.).
2. Export/copy the complete conversation or execution log, preserving failed attempts and corrections.
3. Save it as `ACTUAL_CODING_TOOL_THREAD.md` or PDF in this `docs` folder.
4. Include the tool name and date.
5. If you did not use Claude Code, state which tool you used rather than labelling another tool's history as Claude Code.
