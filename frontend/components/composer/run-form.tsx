"use client";

import { FormEvent, useMemo, useState } from "react";

import { DEFAULT_BRIEF, DEFAULT_CONSTRAINTS } from "@/lib/constants";
import { RunExecutionResult } from "@/lib/types";

import { ConstraintBuilder, ConstraintRow } from "./constraint-builder";
import { RunSubmitBar } from "./run-submit-bar";
import { useCreateRun } from "@/hooks/use-create-run";

type RunFormProps = {
  onSuccess?: (result: RunExecutionResult) => void;
};

function buildConstraintMap(rows: ConstraintRow[]) {
  const entries = rows
    .map((row) => [row.key.trim(), row.value.trim()] as const)
    .filter(([key, value]) => key && value);

  return entries.length ? Object.fromEntries(entries) : null;
}

export function RunForm({ onSuccess }: RunFormProps) {
  const [brief, setBrief] = useState(DEFAULT_BRIEF);
  const [topK, setTopK] = useState(3);
  const [constraints, setConstraints] = useState<ConstraintRow[]>(DEFAULT_CONSTRAINTS);
  const mutation = useCreateRun();

  const helperText = useMemo(() => {
    const activeCount = constraints.filter(
      (row) => row.key.trim() && row.value.trim(),
    ).length;
    return `${activeCount} active constraint${activeCount === 1 ? "" : "s"}`;
  }, [constraints]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    mutation.mutate(
      {
        brief,
        top_k: topK,
        constraints: buildConstraintMap(constraints),
      },
      {
        onSuccess: (result) => {
          onSuccess?.(result);
        },
      },
    );
  };

  return (
    <form className="shell-panel space-y-6" onSubmit={handleSubmit}>
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="eyebrow">Compose a run</div>
          <h2 className="section-title mt-4">Brief the graph like an operator.</h2>
        </div>
        <span className="pill">{helperText}</span>
      </div>

      <label className="block">
        <span className="mb-2 block text-sm font-semibold">Startup brief</span>
        <textarea
          className="textarea-base"
          onChange={(event) => setBrief(event.target.value)}
          placeholder="Find operationally painful B2B software ideas in a narrow market..."
          value={brief}
        />
      </label>

      <div className="grid gap-4 md:grid-cols-[0.45fr_1fr]">
        <label className="block">
          <span className="mb-2 block text-sm font-semibold">Top ideas</span>
          <select
            className="select-base"
            onChange={(event) => setTopK(Number(event.target.value))}
            value={topK}
          >
            <option value={1}>1 idea</option>
            <option value={2}>2 ideas</option>
            <option value={3}>3 ideas</option>
            <option value={4}>4 ideas</option>
            <option value={5}>5 ideas</option>
          </select>
        </label>

        <div className="rounded-[24px] border border-[rgba(31,26,22,0.08)] bg-white/55 p-4">
          <p className="text-sm font-semibold">Guidance</p>
          <p className="mt-2 text-sm leading-6 text-[color:var(--muted)]">
            Strong runs are narrow, buyer-aware, and opinionated. Good example:
            &quot;Find recurring-revenue workflow software ideas for mid-market
            freight brokerages with messy back-office operations.&quot;
          </p>
        </div>
      </div>

      <ConstraintBuilder onChange={setConstraints} rows={constraints} />

      {mutation.isError ? (
        <div className="rounded-[24px] border border-[rgba(200,92,44,0.25)] bg-[rgba(200,92,44,0.08)] p-4 text-sm text-[color:var(--ink)]">
          {mutation.error instanceof Error
            ? mutation.error.message
            : "The run failed to start."}
        </div>
      ) : null}

      <RunSubmitBar pending={mutation.isPending} />
    </form>
  );
}
