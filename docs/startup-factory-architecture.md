# Startup Factory Architecture

This document defines the recommended architecture for the startup idea generation system we discussed.

## Decision Summary

We will build this as a `LangGraph`-first application.

- `LangGraph` is the primary orchestrator and runtime.
- `deepagents` are optional specialist workers inside selected nodes in a later phase.
- `FastAPI` will be the main app interface, with a small CLI for local development.
- `Pydantic` models will define request, state, and output schemas.
- `LangSmith` will be the default tracing and evaluation layer.

## Why This Direction

This workflow already has the shape of a graph:

- explicit stages
- shared state
- conditional routing
- bounded refinement loops
- scoring and ranking

That makes `LangGraph` the best fit for the core architecture.

`deepagents` are still useful, but only for the parts that are open-ended, tool-heavy, or research-driven. For example:

- industry scanning with external search
- competitor validation
- aggressive red-team critique

## System Architecture

```text
Client (CLI / FastAPI / future UI)
        |
        v
Request Validation
        |
        v
LangGraph Orchestrator
        |
        +--> industry_scan
        +--> problem_mine
        +--> quantify_pain
        +--> generate_ideas
        +--> expand_ideas
        +--> critique_ideas
        +--> refine_ideas (conditional loop)
        +--> score_ideas
        +--> finalize_output
        |
        v
Result Serializer
        |
        +--> API response
        +--> JSON artifact
        +--> tracing / evaluation metadata
```

## Planned Graph Flow

```text
input
  -> industry_scan
  -> problem_mine
  -> quantify_pain
  -> generate_ideas
  -> expand_ideas
  -> critique_ideas
  -> refine_ideas? (if critique below threshold and iterations remain)
  -> score_ideas
  -> finalize_output
```

## Node Responsibilities

### `industry_scan`

- Find 5 to 10 industries with current inefficiencies
- Prefer hidden operational pain over generic trends
- Output structured industry findings

### `problem_mine`

- Convert industries into narrow, painful, operational problems
- Avoid vague problem statements
- Output one or more concrete problems per industry

### `quantify_pain`

- Estimate impact in terms of money, time, risk, or headcount drag
- Attach confidence and uncertainty where needed
- Filter out weak or low-frequency problems

### `generate_ideas`

- Map real problems into business ideas
- Constrain generation toward B2B, recurring revenue, and small-team feasibility
- Produce multiple ideas for each validated problem

### `expand_ideas`

- Add ICP, MVP scope, likely buyer, wedge, pricing shape, and go-to-market angle
- Turn raw ideas into buildable concepts

### `critique_ideas`

- Attack assumptions
- Identify why buyers might not care
- Identify why incumbents or existing workflows may win
- Surface risk, commoditization, and adoption friction

### `refine_ideas`

- Improve the idea using critic feedback
- Keep refinement bounded to 2 to 3 passes max

### `score_ideas`

- Score on urgency, willingness to pay, MVP feasibility, defensibility, and evidence quality
- Normalize scores so ideas are comparable

### `finalize_output`

- Return the top ideas
- Include problem, solution, MVP, GTM, critic summary, and final score

## State Model

We should use typed graph state and typed domain models instead of loose dictionaries.

Recommended top-level state:

```python
class WorkflowState(TypedDict, total=False):
    user_brief: str
    constraints: dict
    industries: list[IndustryFinding]
    problems: list[ProblemFinding]
    ideas: list[StartupIdea]
    critiques: list[CritiqueFeedback]
    scores: list[IdeaScore]
    ranked_ideas: list[StartupIdea]
    iteration_count: int
    discarded_idea_ids: list[str]
    final_output: FinalReport
```

Recommended structured models:

- `RunRequest`
- `IndustryFinding`
- `ProblemFinding`
- `PainEstimate`
- `StartupIdea`
- `CritiqueFeedback`
- `IdeaScore`
- `FinalReport`

## Deep Agents: Where They Fit

We should not make the whole application one deep agent.

Instead, we can optionally use deep-agent behavior inside specific nodes later:

- `industry_scan`: for broader search and decomposition
- `validation`: for competitor, Reddit, review, or job-post research
- `critique_ideas`: for stronger adversarial analysis

This gives us a hybrid model:

```text
LangGraph controls the workflow
Deep agents handle selected exploratory subtasks
```

## File Architecture

We should move from a single-file prototype into a package structure like this:

```text
langchain-deepagents/
|-- docs/
|   `-- startup-factory-architecture.md
|-- startup_factory/
|   |-- __init__.py
|   |-- config.py
|   |-- graph.py
|   |-- state.py
|   |-- schemas.py
|   |-- cli.py
|   |-- nodes/
|   |   |-- __init__.py
|   |   |-- industry_scan.py
|   |   |-- problem_mine.py
|   |   |-- quantify_pain.py
|   |   |-- generate_ideas.py
|   |   |-- expand_ideas.py
|   |   |-- critique_ideas.py
|   |   |-- refine_ideas.py
|   |   |-- score_ideas.py
|   |   `-- finalize_output.py
|   |-- prompts/
|   |   |-- industry_scan.txt
|   |   |-- problem_mine.txt
|   |   |-- quantify_pain.txt
|   |   |-- generate_ideas.txt
|   |   |-- critique_ideas.txt
|   |   `-- score_ideas.txt
|   |-- services/
|   |   |-- llm.py
|   |   |-- ranking.py
|   |   |-- persistence.py
|   |   `-- formatting.py
|   |-- tools/
|   |   |-- __init__.py
|   |   |-- research.py
|   |   `-- competitor_check.py
|   `-- api/
|       |-- __init__.py
|       |-- main.py
|       `-- routes.py
|-- tests/
|   |-- test_graph.py
|   |-- test_nodes.py
|   `-- test_scoring.py
|-- .env.example
|-- langgraph.json
|-- requirements.txt
`-- README.md
```

## Tech Stack

### Core runtime

- `Python 3.11`
- `LangGraph`
- `LangChain`
- `langchain-openai`

### API and schemas

- `FastAPI`
- `Pydantic v2`
- `Uvicorn`

### Dev and quality

- `pytest`
- `ruff`

### Observability

- `LangSmith`

### Optional later additions

- search/research provider behind a tool interface
- persistent storage for run history
- deep-agent workers for research-heavy nodes

## Why This Stack

- `LangGraph` gives us state, branching, long-running workflows, and refinement loops.
- `langchain-openai` is a better fit than low-level SDK calls for structured outputs inside graph nodes.
- `Pydantic` gives us typed contracts between nodes.
- `FastAPI` gives us a clean service boundary and an easy path to a UI later.
- `LangSmith` gives us trace visibility when the graph becomes more complex.

## Phase Plan

### Phase 1: Core graph

- industry scan
- problem mining
- idea generation
- critique
- scoring
- final output

### Phase 2: Better structure

- stronger typed schemas
- prompt isolation by node
- saved run artifacts
- API layer

### Phase 3: Validation and research

- external research tools
- competitor checks
- evidence-aware scoring

### Phase 4: Hybrid deep-agent mode

- deep-agent industry research worker
- deep-agent validation worker
- stronger red-team node

## Out of Scope for V1

- multi-user auth
- database-backed memory
- autonomous infinite loops
- full web scraping stack
- deployment-specific infrastructure

## Sources

These choices are based on the official docs below plus implementation judgment:

- LangGraph overview: https://docs.langchain.com/oss/python/langgraph/overview
- LangGraph application structure: https://docs.langchain.com/oss/python/langgraph/application-structure
- Deep Agents overview: https://docs.langchain.com/oss/python/deepagents/overview
- ChatOpenAI integration: https://docs.langchain.com/oss/python/integrations/chat/openai
- Pydantic models: https://docs.pydantic.dev/latest/concepts/models/
- FastAPI bigger applications: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- LangSmith observability: https://docs.langchain.com/oss/python/langgraph/observability
