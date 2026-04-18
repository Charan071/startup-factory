# ISSUE-002 Startup Factory API And Artifacts

- Status: `Done`
- Priority: `High`
- Owner: `Unassigned`

## Summary

Add a shared execution layer, persisted run artifacts, and a FastAPI interface for creating and retrieving startup-factory runs.

## Acceptance Criteria

- CLI and API use the same execution service
- runs can be saved to disk and loaded later by run ID
- FastAPI exposes health and run endpoints
- repo contains a V2 plan version documenting the change

## Notes

- V2 keeps the graph at 6 live nodes
- persistence is local artifact storage, not a database
