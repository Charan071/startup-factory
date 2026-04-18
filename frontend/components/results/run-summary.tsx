import { formatDate } from "@/lib/formatters";
import { FinalReport } from "@/lib/types";

type RunSummaryProps = {
  report: FinalReport;
};

export function RunSummary({ report }: RunSummaryProps) {
  return (
    <section className="shell-panel">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="eyebrow">Latest result</div>
          <h2 className="section-title mt-4 max-w-3xl">{report.brief}</h2>
        </div>
        <div className="rounded-[24px] border border-[rgba(21,118,108,0.16)] bg-[rgba(21,118,108,0.08)] px-4 py-3 text-right">
          <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--teal)]">
            Generated
          </p>
          <p className="mt-2 text-sm font-semibold">{formatDate(report.generated_at)}</p>
        </div>
      </div>

      <div className="mt-6 grid gap-3 sm:grid-cols-3">
        <div className="stat-chip">
          <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
            Top ideas
          </p>
          <p className="mt-2 text-lg font-semibold">{report.top_ideas.length}</p>
        </div>
        <div className="stat-chip">
          <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
            Highest score
          </p>
          <p className="mt-2 text-lg font-semibold">
            {report.top_ideas[0]?.score.toFixed(1) ?? "--"}
          </p>
        </div>
        <div className="stat-chip">
          <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
            Delivery mode
          </p>
          <p className="mt-2 text-lg font-semibold">Artifact backed</p>
        </div>
      </div>
    </section>
  );
}
