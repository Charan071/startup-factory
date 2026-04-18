import type { Metadata } from "next";
import { DM_Sans, Fraunces } from "next/font/google";
import { ReactNode } from "react";

import { AppShell } from "@/components/layout/app-shell";

import "./globals.css";
import { Providers } from "./providers";

const bodyFont = DM_Sans({
  subsets: ["latin"],
  variable: "--font-body",
});

const displayFont = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
});

export const metadata: Metadata = {
  title: "Startup Factory V3",
  description:
    "A LangGraph-powered startup idea studio with a FastAPI backend and Next.js frontend.",
};

type RootLayoutProps = {
  children: ReactNode;
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <body className={`${bodyFont.variable} ${displayFont.variable} antialiased`}>
        <Providers>
          <AppShell>{children}</AppShell>
        </Providers>
      </body>
    </html>
  );
}
