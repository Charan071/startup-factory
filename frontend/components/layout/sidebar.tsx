"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "Studio", description: "Compose and run the graph" },
  { href: "/runs", label: "Archive", description: "Inspect saved artifacts" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="border-b border-[rgba(31,26,22,0.08)] bg-[rgba(255,248,239,0.75)] px-4 py-4 backdrop-blur lg:fixed lg:inset-y-0 lg:left-0 lg:w-[288px] lg:border-b-0 lg:border-r lg:px-5 lg:py-6">
      <div className="shell-surface flex h-full flex-col gap-5 p-5">
        <div>
          <div className="eyebrow">Startup factory</div>
          <h1 className="font-display mt-4 text-3xl leading-tight">
            Studio desk for startup pattern-finding.
          </h1>
          <p className="muted-copy mt-4">
            V3 puts the graph, artifacts, and ranked ideas in one workspace.
          </p>
        </div>

        <nav className="space-y-3">
          {navItems.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                className={`block rounded-[24px] border p-4 transition-colors ${
                  active
                    ? "border-[rgba(200,92,44,0.28)] bg-[rgba(200,92,44,0.08)]"
                    : "border-[rgba(31,26,22,0.08)] bg-white/45 hover:bg-white/70"
                }`}
                href={item.href}
              >
                <p className="text-sm font-semibold">{item.label}</p>
                <p className="mt-1 text-sm text-[color:var(--muted)]">
                  {item.description}
                </p>
              </Link>
            );
          })}
        </nav>

        <div className="mt-auto rounded-[24px] border border-[rgba(35,86,160,0.14)] bg-[rgba(35,86,160,0.08)] p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--secondary)]">
            Active stack
          </p>
          <ul className="mt-3 space-y-2 text-sm leading-6 text-[color:var(--ink)]">
            <li>FastAPI API layer</li>
            <li>LangGraph workflow engine</li>
            <li>TanStack Query data client</li>
          </ul>
        </div>
      </div>
    </aside>
  );
}
