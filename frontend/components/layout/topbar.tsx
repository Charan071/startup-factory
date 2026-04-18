export function Topbar() {
  return (
    <header className="px-4 pt-4 md:px-8 lg:px-10">
      <div className="shell-surface flex flex-col gap-4 px-5 py-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[color:var(--secondary)]">
            FastAPI + Next.js
          </p>
          <p className="mt-2 text-sm text-[color:var(--muted)]">
            Frontend and backend stay separate on purpose: the UI is a client
            for the graph runtime, not a replacement for it.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <span className="nav-chip">LangGraph orchestration</span>
          <span className="nav-chip">Artifact-backed runs</span>
          <span className="nav-chip">Critic-first scoring</span>
        </div>
      </div>
    </header>
  );
}
