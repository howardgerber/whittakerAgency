# Project-Specific Reminders for Claude

## Frontend Build Process

⚠️ **IMPORTANT: Always use the dev build script to avoid CORS errors**

**DO THIS:**
```bash
cd scripts && ./frontend-build-dev.bat
```
This runs `npm run build:dev` which builds with the correct API configuration for development.

**DON'T DO THIS:**
```bash
cd frontend && npm run build  # ❌ This is production build and causes CORS errors
```

## Why?
- The dev build uses `--mode development` which configures the correct API URLs
- Production build points to different API endpoints and causes CORS issues
- The `frontend-build-dev.bat` script is specifically set up for local development

## When to Use Each Build

- **Local Development/Testing**: `./scripts/frontend-build-dev.bat`
- **Production Deployment**: Only use production build when explicitly deploying to production

## Code Review Process

⚠️ **For code-reviewer agent**:
- **ALWAYS** start by reading `docs/TECHNICAL-DEBT.md` before reviewing code
- Check if any existing issues in the document have been fixed
- After review, update `docs/TECHNICAL-DEBT.md` with:
  - Remove fixed issues
  - Add new issues found
  - Update the issue count in the header
  - Update the "Last Updated" date

## Architecture Review Process

⚠️ **For architecture-optimizer agent**:
- **ALWAYS** start by reading `docs/ARCHITECTURE-REVIEW.md` before reviewing architecture
- Check if any existing findings have been addressed
- After review, update `docs/ARCHITECTURE-REVIEW.md` with:
  - Remove fixed issues
  - Add new findings
  - Update the issue count in the header
  - Update the "Last Updated" date
- **Be VERBOSE and EDUCATIONAL**: This is a learning document
  - Explain WHY each change is important, not just what to change
  - Include background on concepts (e.g., "N+1 queries", "race conditions", "eventual consistency")
  - Explain the trade-offs and consequences of different approaches
  - Use examples to illustrate the impact
  - Assume the reader is learning and wants to understand the reasoning
- Format: `### [Short Title]` followed by detailed explanation with Files/Problem/Why It Matters/Impact/Fix/Learn More sections

## Documentation Formatting Rules

⚠️ **For doc-reviewer agent**:

**For `docs/TECHNICAL-DEBT.md`**:
- **NEVER** add numbers to issues
- Use bullet points (###) for issue titles, NOT numbered lists
- Keep it CONCISE and scannable
- Format: `### [Short Title]` with brief bullets for Files/Problem/Impact/Fix
- Maintain severity sections (CRITICAL, HIGH, MEDIUM, LOW)

**For `docs/ARCHITECTURE-REVIEW.md`**:
- **NEVER** add numbers to issues
- Use bullet points (###) for issue titles, NOT numbered lists
- Keep it VERBOSE and EDUCATIONAL - do NOT make it more concise
- Preserve all "Why It Matters" and "Learn More" sections
- This document is for learning, not just task tracking
- Format: `### [Short Title]` with detailed explanation sections

## Other Project Conventions

- **Database Changes**: When schema changes are made pre-production, drop and recreate DB rather than migrations
- **Commit Process**: Only commit when user explicitly requests it (don't be proactive)
- **Category/Subcategory Display**: Always show the most specific name/icon (subcategory if exists, else category)
- **Forms**: All "Other" category forms are now complete (7/7 done)
