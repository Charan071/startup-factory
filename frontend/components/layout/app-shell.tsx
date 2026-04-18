import { ReactNode } from "react";

import { Sidebar } from "./sidebar";
import { Topbar } from "./topbar";

type AppShellProps = {
  children: ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen">
      <Sidebar />
      <div className="lg:pl-[288px]">
        <Topbar />
        <main className="px-4 pb-10 pt-4 md:px-8 lg:px-10">{children}</main>
      </div>
    </div>
  );
}
