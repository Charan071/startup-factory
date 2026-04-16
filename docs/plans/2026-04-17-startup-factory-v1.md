# Startup Factory V1

- Date: `2026-04-17`
- Version: `v1`
- Status: `Active`

## Goal

Ship a small, inspectable `LangGraph` startup-idea generator with typed schemas, versioned plan docs, and a markdown issue backlog.

## Decisions

- `docs/startup-factory-architecture.md` remains the canonical architecture document
- versioned implementation plans live under `docs/plans/`
- issues are tracked as markdown files under `issues/`
- V1 is CLI only
- V1 uses `LangGraph` plus the wrapped `openai` client for optional LangSmith tracing
- V1 does not include a database, FastAPI, deep-agent workers, or web research tools

## Deliverables

- `docs/plans/index.md`
- `issues/index.md`
- `issues/ISSUE-001-startup-factory-mvp.md`
- `startup_factory/` package with graph, nodes, prompts, schemas, state, and CLI
- tests for schemas, graph behavior, CLI output, and docs layout

## Risks

- model output can drift if prompts become too loose
- scoring quality depends on how well the critic and scorer prompts stay grounded
- without research tools, V1 ideas may still need manual real-world validation

## Next Steps

1. scaffold `startup_factory`
2. validate CLI output with mocked tests
3. use LangSmith traces to tighten prompts if outputs become generic
