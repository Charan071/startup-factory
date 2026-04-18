# ISSUE-003 Startup Factory Frontend V3

- Status: `Done`
- Priority: `High`
- Owner: `Unassigned`

## Summary

Build the V3 frontend using `Next.js`, `TypeScript`, `Tailwind CSS`, and `TanStack Query`, while keeping `FastAPI` as the backend API layer for the existing `LangGraph` runtime.

## Acceptance Criteria

- `frontend/` is scaffolded with the approved stack
- the UI can create a run, view a saved run, and browse run history
- the frontend talks to `startup_factory/api/` rather than replacing it
- backend adds the minimal API changes needed for UI support
- the visual direction matches the approved warm, premium dashboard mockup

## Notes

- `FastAPI` remains in use as the backend service layer
- `Next.js` is the frontend application layer
- V3 should keep the current sync run model first, then evolve to async later if needed
- V3 now includes the dashboard, saved run archive, and run detail pages backed by the FastAPI endpoints
