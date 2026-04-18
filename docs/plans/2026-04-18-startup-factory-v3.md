# Startup Factory V3

- Date: `2026-04-18`
- Version: `v3`
- Status: `Active`

## Goal

Add a real product frontend for `startup_factory` while keeping `FastAPI` as the backend API layer and `LangGraph` as the orchestration core.

## Decisions

- use `Next.js` + `TypeScript` + `Tailwind CSS` + `TanStack Query` for the frontend
- keep `FastAPI` as the backend API because the graph runtime is already implemented in Python
- frontend and backend stay separate:
  - `frontend/` for the Next.js app
  - `startup_factory/api/` for the FastAPI layer
- V3 does not replace `FastAPI`; it adds a UI on top of it
- V3 keeps the current synchronous run model first, then adds UI-friendly API improvements for run history and polling readiness

## Why FastAPI Still Matters

We are already using `FastAPI` in V2:

- `startup_factory/api/main.py`
- `startup_factory/api/routes.py`

It is the backend service layer for:

- creating runs
- loading saved runs
- exposing health and future UI-facing endpoints

`Next.js` is the frontend application, not the graph runtime. The clean split is:

- `Next.js` renders the product UI
- `TanStack Query` calls the API
- `FastAPI` executes or loads runs
- `LangGraph` performs the actual workflow

## Frontend Scope

V3 frontend should include:

- landing/dashboard page for entering a startup brief
- run composer with:
  - brief textarea
  - `top_k` selector
  - constraints builder
  - save-artifact toggle
- live run view with:
  - pipeline progress strip
  - active/loading states
  - ranked idea cards
  - score breakdown chips
  - critic summary blocks
- run details page for a saved run ID
- run history page backed by saved artifact metadata
- empty, loading, and API-error states

V3 frontend should not include:

- auth
- multi-user accounts
- billing
- admin tools
- deep-agent controls

## Frontend File Structure

```text
frontend/
|-- app/
|   |-- layout.tsx
|   |-- page.tsx
|   |-- runs/
|   |   |-- page.tsx
|   |   `-- [runId]/
|   |       `-- page.tsx
|   |-- globals.css
|   `-- providers.tsx
|-- components/
|   |-- layout/
|   |   |-- sidebar.tsx
|   |   |-- topbar.tsx
|   |   `-- app-shell.tsx
|   |-- composer/
|   |   |-- run-form.tsx
|   |   |-- constraint-builder.tsx
|   |   `-- run-submit-bar.tsx
|   |-- results/
|   |   |-- run-summary.tsx
|   |   |-- idea-card.tsx
|   |   |-- score-breakdown.tsx
|   |   |-- pipeline-strip.tsx
|   |   `-- artifact-panel.tsx
|   |-- runs/
|   |   |-- run-history-table.tsx
|   |   `-- run-status-badge.tsx
|-- lib/
|   |-- api.ts
|   |-- query-client.ts
|   |-- types.ts
|   |-- formatters.ts
|   `-- constants.ts
|-- hooks/
|   |-- use-create-run.ts
|   |-- use-run.ts
|   `-- use-runs.ts
|-- .env.local.example
|-- package.json
|-- tsconfig.json
|-- postcss.config.mjs
`-- next.config.ts
```

## Backend API Changes Needed For UI Support

Keep existing endpoints:

- `GET /api/v1/health`
- `POST /api/v1/runs`
- `GET /api/v1/runs/{run_id}`

Add these UI-supporting endpoints in V3:

- `GET /api/v1/runs`
  - returns recent saved runs as summaries for the history page
- `GET /api/v1/runs/{run_id}/summary`
  - lightweight metadata for fast page loads

Add these backend changes:

- enable CORS for local Next.js development
  - allow `http://localhost:3000`
- return UI-safe metadata instead of exposing raw filesystem assumptions as the only artifact reference
- standardize response shapes for loading result pages:
  - run id
  - created timestamp
  - brief
  - top idea titles
  - score snapshot
- preserve the existing sync `POST /runs` behavior for V3
- structure backend code so async/polling can be added in V4 without rewriting route contracts

## Frontend Data Flow

1. user submits a brief in Next.js
2. frontend sends `POST /api/v1/runs`
3. backend runs the `LangGraph` workflow through the existing service layer
4. backend saves artifact metadata and returns `RunExecutionResult`
5. frontend renders:
   - pipeline state
   - ranked ideas
   - saved run information
6. history page uses `GET /api/v1/runs`
7. details page uses `GET /api/v1/runs/{run_id}`

## Visual Design Direction

The frontend should follow the mockup direction already established:

- warm cream and parchment surfaces
- black ink typography
- burnt-orange as the main accent
- cobalt blue as the secondary accent
- teal for success/progress states
- no dark mode for V3
- no purple bias

UI layout should feel like a premium product dashboard:

- left navigation rail
- top status/search bar
- large prompt composer in the hero area
- horizontal graph pipeline progress strip
- ranked startup idea cards as the primary content
- secondary side panels for:
  - run artifact
  - trace timeline
  - validation signals

Typography and motion:

- bold, expressive display typography
- mono accents for run IDs, node names, and API labels
- restrained but meaningful motion:
  - loading shimmer
  - step progress transitions
  - card reveal/stagger

## Deliverables

- V3 plan doc in `docs/plans/`
- update plans index and README to point at V3
- open V3 issue for frontend and backend UI support
- implement `frontend/` with dashboard, archive, and run detail pages
- add run summary endpoints and CORS support in `FastAPI`
- verify the frontend build and backend test suite

## Risks

- synchronous run execution may feel slow in the browser for longer prompts
- UI quality can collapse into generic dashboard patterns if we do not preserve the mockup direction
- artifact path handling needs a cleaner API abstraction before exposing too much backend detail to the browser

## Next Steps

1. evaluate V4 scope around stronger research validation and async job execution
2. add richer progress states if graph latency starts to feel heavy in the browser
3. decide whether saved artifacts should stay file-backed or move behind a database later
