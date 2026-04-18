import { PIPELINE_STAGES } from "@/lib/constants";

export function PipelineStrip() {
  return (
    <section className="shell-panel overflow-hidden">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="eyebrow">Pipeline</div>
          <h2 className="section-title mt-4">Visible graph, not hidden magic.</h2>
        </div>
        <p className="muted-copy max-w-xl">
          Each stage represents a real node in the workflow so the user can
          reason about where a weak idea came from.
        </p>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-5">
        {PIPELINE_STAGES.map((stage, index) => (
          <div
            key={stage.id}
            className="rounded-[24px] border border-[rgba(31,26,22,0.08)] bg-white/60 p-4"
          >
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--secondary)]">
              Step {index + 1}
            </p>
            <h3 className="mt-3 text-sm font-semibold">{stage.label}</h3>
            <p className="mt-2 text-sm leading-6 text-[color:var(--muted)]">
              {stage.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
