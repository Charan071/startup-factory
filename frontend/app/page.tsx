"use client";

import { useState } from "react";

import { RunForm } from "@/components/composer/run-form";
import { ArtifactPanel } from "@/components/results/artifact-panel";
import { IdeaCard } from "@/components/results/idea-card";
import { PipelineStrip } from "@/components/results/pipeline-strip";
import { RunSummary } from "@/components/results/run-summary";
import { RunHistoryTable } from "@/components/runs/run-history-table";
import { useRuns } from "@/hooks/use-runs";
import { RunExecutionResult } from "@/lib/types";

export default function HomePage() {
  const [latestRun, setLatestRun] = useState<RunExecutionResult | null>(null);
  const runsQuery = useRuns(6);

  return (
    <div className="space-y-8">
      <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="shell-panel overflow-hidden">
          <div className="eyebrow">V3 studio</div>
          <div className="mt-5 max-w-3xl">
            <h1 className="display-title">
              Turn a vague market hunch into ranked, critic-tested startup ideas.
            </h1>
            <p className="muted-copy mt-4 max-w-2xl">
              Startup Factory combines LangGraph orchestration, an adversarial
              scoring loop, FastAPI, and a front-end workspace designed to make
              each run feel inspectable instead of magical.
            </p>
          </div>
          <div className="mt-6 grid gap-3 sm:grid-cols-3">
            <div className="stat-chip">
              <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
                Workflow
              </p>
              <p className="mt-2 text-sm font-semibold">
                Scan, mine, generate, critique, score
              </p>
            </div>
            <div className="stat-chip">
              <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
                Backend
              </p>
              <p className="mt-2 text-sm font-semibold">FastAPI + LangGraph</p>
            </div>
            <div className="stat-chip">
              <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
                Frontend
              </p>
              <p className="mt-2 text-sm font-semibold">
                Next.js + TanStack Query
              </p>
            </div>
          </div>
        </div>

        <div className="shell-panel flex flex-col justify-between">
          <div>
            <div className="eyebrow">Design direction</div>
            <h2 className="section-title mt-4">
              Editorial warmth with operator-grade structure.
            </h2>
            <p className="muted-copy mt-4">
              The interface leans into paper-toned surfaces, bold serif headers,
              and a visible pipeline so the graph feels legible. The goal is not
              generic dashboard chrome. It should feel like a studio desk for
              startup pattern-finding.
            </p>
          </div>
          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            <div className="rounded-3xl border border-[rgba(31,26,22,0.1)] bg-[rgba(35,86,160,0.08)] p-4">
              <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--secondary)]">
                Look
              </p>
              <p className="mt-2 text-sm font-medium">
                Burnt orange accents, cobalt notes, parchment surfaces
              </p>
            </div>
            <div className="rounded-3xl border border-[rgba(31,26,22,0.1)] bg-[rgba(21,118,108,0.08)] p-4">
              <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--teal)]">
                Outcome
              </p>
              <p className="mt-2 text-sm font-medium">
                Ranked ideas with artifacts and run history
              </p>
            </div>
          </div>
        </div>
      </section>

      <PipelineStrip />

      <section className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <RunForm onSuccess={setLatestRun} />

        <div className="space-y-6">
          <div className="shell-panel">
            <div className="flex items-center justify-between gap-4">
              <div>
                <div className="eyebrow">Saved runs</div>
                <h2 className="section-title mt-4">Recent run history</h2>
              </div>
              <a className="ghost-button" href="/runs">
                Open archive
              </a>
            </div>
            <div className="mt-5">
              <RunHistoryTable
                compact
                loading={runsQuery.isLoading}
                runs={runsQuery.data?.runs ?? []}
              />
            </div>
          </div>

          <div className="shell-panel">
            <div className="eyebrow">What V3 adds</div>
            <ul className="mt-5 space-y-3 text-sm leading-6 text-[color:var(--muted)]">
              <li>Next.js dashboard for briefs, constraints, and result review</li>
              <li>TanStack Query-powered run creation, history, and detail pages</li>
              <li>FastAPI endpoints for listing saved artifacts and summaries</li>
              <li>UI treatment that exposes the graph instead of hiding it</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[0.72fr_1.28fr]">
        <ArtifactPanel savedRun={latestRun?.saved_run ?? null} />

        <div className="space-y-6">
          {latestRun ? (
            <>
              <RunSummary report={latestRun.report} />
              <div className="grid gap-5">
                {latestRun.report.top_ideas.map((idea, index) => (
                  <IdeaCard key={`${idea.title}-${index}`} idea={idea} rank={index + 1} />
                ))}
              </div>
            </>
          ) : (
            <div className="shell-panel">
              <div className="eyebrow">Result workspace</div>
              <h2 className="section-title mt-4">Your next run will land here.</h2>
              <p className="muted-copy mt-4 max-w-2xl">
                Submit a brief and the right column will fill with the saved
                artifact, ranked idea cards, and the score breakdowns that came
                out of the graph run.
              </p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
