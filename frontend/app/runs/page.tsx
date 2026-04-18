"use client";

import { RunHistoryTable } from "@/components/runs/run-history-table";
import { useRuns } from "@/hooks/use-runs";

export default function RunsPage() {
  const runsQuery = useRuns(50);

  return (
    <div className="space-y-6">
      <section className="shell-panel">
        <div className="eyebrow">Archive</div>
        <h1 className="display-title mt-4">Saved run history</h1>
        <p className="muted-copy mt-4 max-w-3xl">
          Each run is stored as a JSON artifact on the backend and surfaced here
          so you can reopen strong ideas, compare briefs, and move from ad hoc
          prompting into a repeatable startup-finding workflow.
        </p>
      </section>

      <RunHistoryTable
        loading={runsQuery.isLoading}
        runs={runsQuery.data?.runs ?? []}
      />
    </div>
  );
}
