# Startup Factory V2

- Date: `2026-04-18`
- Version: `v2`
- Status: `Active`

## Goal

Extend the V1 graph runtime with a reusable service layer, saved run artifacts, and a FastAPI surface without changing the core 6-node graph.

## Decisions

- keep the current graph nodes unchanged for V2
- add a shared execution service used by both CLI and API
- save run artifacts to disk by default under `artifacts/startup_factory/`
- expose a small FastAPI interface for health, create-run, and load-run
- move the OpenAI runtime into a service module so the graph orchestration stays thinner

## Deliverables

- `startup_factory/services/`
- `startup_factory/api/`
- persisted run artifact support
- V2 plan version added to `docs/plans/`
- tests for persistence and API behavior

## Risks

- artifact storage will grow over time without pruning
- API shape is intentionally small and may evolve in V3
- saved local artifacts are not a substitute for a database if multi-user behavior is added later

## Next Steps

1. add the remaining graph stages: `quantify_pain`, `expand_ideas`, `refine_ideas`
2. add research and competitor validation tools
3. improve scoring with stronger evidence checks
