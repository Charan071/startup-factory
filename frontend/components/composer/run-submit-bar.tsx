type RunSubmitBarProps = {
  pending: boolean;
};

export function RunSubmitBar({ pending }: RunSubmitBarProps) {
  return (
    <div className="flex flex-col gap-3 border-t border-[rgba(31,26,22,0.08)] pt-5 sm:flex-row sm:items-center sm:justify-between">
      <p className="text-sm text-[color:var(--muted)]">
        The run saves to the backend artifact store so it can be reopened from
        the archive.
      </p>
      <button className="primary-button" disabled={pending} type="submit">
        {pending ? "Running graph..." : "Generate ranked ideas"}
      </button>
    </div>
  );
}
