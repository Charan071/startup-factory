import { ScoreBreakdown as ScoreBreakdownType } from "@/lib/types";

type ScoreBreakdownProps = {
  breakdown: ScoreBreakdownType;
};

const metricLabels: Array<keyof ScoreBreakdownType> = [
  "urgency",
  "willingness_to_pay",
  "feasibility",
  "defensibility",
];

export function ScoreBreakdown({ breakdown }: ScoreBreakdownProps) {
  return (
    <div className="space-y-3">
      {metricLabels.map((metric) => {
        const value = breakdown[metric];
        return (
          <div key={metric} className="space-y-1.5">
            <div className="flex items-center justify-between text-sm">
              <span className="capitalize text-[color:var(--muted)]">
                {metric.replaceAll("_", " ")}
              </span>
              <span className="font-semibold">{value}/10</span>
            </div>
            <div className="h-2 rounded-full bg-[rgba(31,26,22,0.08)]">
              <div
                className="h-full rounded-full"
                style={{
                  width: `${value * 10}%`,
                  background:
                    metric === "feasibility"
                      ? "linear-gradient(90deg, rgba(21,118,108,0.85), rgba(21,118,108,0.55))"
                      : metric === "defensibility"
                        ? "linear-gradient(90deg, rgba(35,86,160,0.85), rgba(35,86,160,0.55))"
                        : "linear-gradient(90deg, rgba(200,92,44,0.9), rgba(200,92,44,0.55))",
                }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}
