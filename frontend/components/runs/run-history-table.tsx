import Link from "next/link";

import { formatDate } from "@/lib/formatters";
import { RunSummary } from "@/lib/types";

import { RunStatusBadge } from "./run-status-badge";

type RunHistoryTableProps = {
  runs: RunSummary[];
  loading?: boolean;
  compact?: boolean;
};

export function RunHistoryTable({
  runs,
  loading = false,
  compact = false,
}: RunHistoryTableProps) {
  if (loading) {
    return (
      <div className="shell-panel">
        <p className="muted-copy">Loading saved runs...</p>
      </div>
    );
  }

  if (!runs.length) {
    return (
      <div className="shell-panel">
        <p className="muted-copy">
          No saved runs yet. Create one from the studio and it will show up here.
        </p>
      </div>
    );
  }

  return (
    <div className={compact ? "" : "shell-panel"}>
      <div className="overflow-x-auto">
        <table className="min-w-full border-separate border-spacing-y-3">
          <thead>
            <tr className="text-left text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
              <th className="px-3 py-2 font-medium">Brief</th>
              <th className="px-3 py-2 font-medium">Created</th>
              <th className="px-3 py-2 font-medium">Top ideas</th>
              <th className="px-3 py-2 font-medium">Signal</th>
              <th className="px-3 py-2 font-medium">Open</th>
            </tr>
          </thead>
          <tbody>
            {runs.map((run) => (
              <tr
                key={run.run_id}
                className="rounded-[20px] border border-[rgba(31,26,22,0.08)] bg-white/62"
              >
                <td className="rounded-l-[20px] px-3 py-4 align-top">
                  <p className="max-w-md text-sm font-semibold">{run.brief}</p>
                  <p className="mt-1 text-xs text-[color:var(--muted)]">
                    {run.artifact_name}
                  </p>
                </td>
                <td className="px-3 py-4 align-top text-sm text-[color:var(--muted)]">
                  {formatDate(run.created_at)}
                </td>
                <td className="px-3 py-4 align-top">
                  <div className="flex flex-wrap gap-2">
                    {run.top_idea_titles.slice(0, compact ? 2 : 3).map((title) => (
                      <span
                        key={title}
                        className="nav-chip bg-[rgba(35,86,160,0.08)] text-[color:var(--secondary)]"
                      >
                        {title}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="px-3 py-4 align-top">
                  <RunStatusBadge topScore={run.top_score} />
                </td>
                <td className="rounded-r-[20px] px-3 py-4 align-top">
                  <Link className="ghost-button" href={`/runs/${run.run_id}`}>
                    View run
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
