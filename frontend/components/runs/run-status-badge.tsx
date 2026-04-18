type RunStatusBadgeProps = {
  topScore: number | null | undefined;
};

export function RunStatusBadge({ topScore }: RunStatusBadgeProps) {
  const label =
    typeof topScore !== "number"
      ? "Needs review"
      : topScore >= 8.5
        ? "High potential"
        : topScore >= 7.5
          ? "Worth testing"
          : "Exploratory";

  const styles =
    typeof topScore !== "number"
      ? "bg-[rgba(31,26,22,0.08)] text-[color:var(--muted)]"
      : topScore >= 8.5
        ? "bg-[rgba(21,118,108,0.12)] text-[color:var(--teal)]"
        : topScore >= 7.5
          ? "bg-[rgba(35,86,160,0.12)] text-[color:var(--secondary)]"
          : "bg-[rgba(200,92,44,0.12)] text-[color:var(--accent)]";

  return (
    <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${styles}`}>
      {label}
    </span>
  );
}
