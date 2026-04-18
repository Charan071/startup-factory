"use client";

import { useQuery } from "@tanstack/react-query";

import { getRuns } from "@/lib/api";

export function useRuns(limit = 20) {
  return useQuery({
    queryKey: ["runs", limit],
    queryFn: () => getRuns(limit),
  });
}
