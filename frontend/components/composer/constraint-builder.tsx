"use client";

export type ConstraintRow = {
  id: string;
  key: string;
  value: string;
};

type ConstraintBuilderProps = {
  rows: ConstraintRow[];
  onChange: (rows: ConstraintRow[]) => void;
};

export function ConstraintBuilder({
  rows,
  onChange,
}: ConstraintBuilderProps) {
  const updateRow = (
    rowId: string,
    field: "key" | "value",
    nextValue: string,
  ) => {
    onChange(
      rows.map((row) =>
        row.id === rowId ? { ...row, [field]: nextValue } : row,
      ),
    );
  };

  const addRow = () => {
    onChange([
      ...rows,
      { id: crypto.randomUUID(), key: "", value: "" },
    ]);
  };

  const removeRow = (rowId: string) => {
    onChange(rows.filter((row) => row.id !== rowId));
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold">Constraints</p>
          <p className="mt-1 text-sm text-[color:var(--muted)]">
            Use them to force the idea search into a sharper operating frame.
          </p>
        </div>
        <button className="ghost-button" onClick={addRow} type="button">
          Add row
        </button>
      </div>

      <div className="space-y-3">
        {rows.map((row) => (
          <div
            key={row.id}
            className="grid gap-3 rounded-[24px] border border-[rgba(31,26,22,0.08)] bg-white/55 p-4 md:grid-cols-[0.9fr_1.1fr_auto]"
          >
            <input
              className="input-base"
              onChange={(event) => updateRow(row.id, "key", event.target.value)}
              placeholder="constraint key"
              value={row.key}
            />
            <input
              className="input-base"
              onChange={(event) =>
                updateRow(row.id, "value", event.target.value)
              }
              placeholder="constraint value"
              value={row.value}
            />
            <button
              className="ghost-button"
              onClick={() => removeRow(row.id)}
              type="button"
            >
              Remove
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
