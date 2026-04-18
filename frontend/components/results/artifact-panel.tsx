import Link from "next/link";

import { formatDate, truncateMiddle } from "@/lib/formatters";
import { SavedRun } from "@/lib/types";

type ArtifactPanelProps = {
  savedRun: SavedRun | null;
};

export function ArtifactPanel({ savedRun }: ArtifactPanelProps) {
  return (
    <aside className="shell-panel h-fit">
      <div className="eyebrow">Artifact</div>
      {savedRun ? (
        <>
          <h2 className="section-title mt-4">Run saved to disk and API archive.</h2>
          <dl className="mt-6 space-y-4">
            <div>
              <dt className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
                Run id
              </dt>
              <dd className="mt-2 text-sm font-medium">
                {truncateMiddle(savedRun.run_id, 18)}
              </dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
                Artifact name
              </dt>
              <dd className="mt-2 text-sm font-medium">
                {savedRun.artifact_name ?? "Artifact unavailable"}
              </dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
                Created
              </dt>
              <dd className="mt-2 text-sm font-medium">
                {savedRun.created_at ? formatDate(savedRun.created_at) : "Unknown"}
              </dd>
            </div>
          </dl>

          <div className="mt-6 flex flex-wrap gap-3">
            <Link className="primary-button" href={`/runs/${savedRun.run_id}`}>
              Open detail view
            </Link>
          </div>
        </>
      ) : (
        <>
          <h2 className="section-title mt-4">No artifact yet.</h2>
          <p className="muted-copy mt-4">
            Submit a run and this panel will show the saved artifact id and the
            shortcut into the detailed results page.
          </p>
        </>
      )}
    </aside>
  );
}
