import { StartupIdea } from "@/lib/types";

import { ScoreBreakdown } from "./score-breakdown";

type IdeaCardProps = {
  idea: StartupIdea;
  rank: number;
};

export function IdeaCard({ idea, rank }: IdeaCardProps) {
  return (
    <article className="shell-panel">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="eyebrow">Rank {rank}</div>
          <h3 className="section-title mt-4">{idea.title}</h3>
          <p className="mt-3 text-sm font-medium text-[color:var(--secondary)]">
            {idea.industry}
          </p>
        </div>
        <div className="rounded-[24px] border border-[rgba(200,92,44,0.18)] bg-[rgba(200,92,44,0.08)] px-4 py-3 text-right">
          <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--accent)]">
            Overall score
          </p>
          <p className="mt-2 text-2xl font-semibold">{idea.score.toFixed(1)}</p>
        </div>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <div className="space-y-5">
          <div>
            <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
              Problem
            </p>
            <p className="mt-2 text-sm leading-6">{idea.problem}</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
              Solution
            </p>
            <p className="mt-2 text-sm leading-6">{idea.solution}</p>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            <div>
              <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
                ICP
              </p>
              <p className="mt-2 text-sm leading-6">{idea.icp}</p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
                MVP
              </p>
              <p className="mt-2 text-sm leading-6">{idea.mvp}</p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
                GTM
              </p>
              <p className="mt-2 text-sm leading-6">{idea.gtm}</p>
            </div>
          </div>
        </div>

        <div className="rounded-[28px] border border-[rgba(31,26,22,0.08)] bg-white/60 p-5">
          <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--teal)]">
            Critic summary
          </p>
          <p className="mt-3 text-sm leading-6">{idea.critic_summary}</p>
          <div className="mt-6">
            <ScoreBreakdown breakdown={idea.score_breakdown} />
          </div>
        </div>
      </div>
    </article>
  );
}
