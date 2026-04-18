"use client";

import Link from "next/link";
import { useParams } from "next/navigation";

import { ArtifactPanel } from "@/components/results/artifact-panel";
import { IdeaCard } from "@/components/results/idea-card";
import { PipelineStrip } from "@/components/results/pipeline-strip";
import { RunSummary } from "@/components/results/run-summary";
import { useRun } from "@/hooks/use-run";

export default function RunDetailPage() {
  const params = useParams<{ runId: string }>();
  const runId = Array.isArray(params.runId) ? params.runId[0] : params.runId;
  const runQuery = useRun(runId);

  if (runQuery.isLoading) {
    return (
      <div className="shell-panel">
        <div className="eyebrow">Loading</div>
        <p className="muted-copy mt-4">Rehydrating saved run artifact...</p>
      </div>
    );
  }

  if (runQuery.isError || !runQuery.data) {
    return (
      <div className="shell-panel">
        <div className="eyebrow">Run not found</div>
        <h1 className="section-title mt-4">This saved run could not be loaded.</h1>
        <p className="muted-copy mt-4">
          The backend may not have the artifact anymore, or the run id may be
          incorrect.
        </p>
        <Link className="ghost-button mt-6" href="/runs">
          Back to archive
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <section className="shell-panel">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="eyebrow">Saved run</div>
            <h1 className="display-title mt-4 max-w-4xl">
              {runQuery.data.request.brief}
            </h1>
          </div>
          <Link className="ghost-button" href="/runs">
            Back to archive
          </Link>
        </div>
      </section>

      <PipelineStrip />

      <section className="grid gap-6 xl:grid-cols-[0.72fr_1.28fr]">
        <ArtifactPanel savedRun={runQuery.data.saved_run} />

        <div className="space-y-6">
          <RunSummary report={runQuery.data.report} />
          <div className="grid gap-5">
            {runQuery.data.report.top_ideas.map((idea, index) => (
              <IdeaCard key={`${idea.title}-${index}`} idea={idea} rank={index + 1} />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
