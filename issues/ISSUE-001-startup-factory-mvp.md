# ISSUE-001 Startup Factory MVP

- Status: `Open`
- Priority: `High`
- Owner: `Unassigned`

## Summary

Build the first runnable `startup_factory` CLI that turns a user brief into ranked B2B startup ideas using a `LangGraph` workflow.

## Acceptance Criteria

- package contains typed schemas, state, graph, prompts, and CLI
- CLI returns ranked ideas in markdown or JSON
- tracing works through environment variables only
- repo contains versioned plan docs and issue indexes
- no legacy recurring-status folder or related references are introduced

## Notes

- keep the existing PDF Q&A example unchanged
- keep V1 small and debuggable before adding research tools or persistence
