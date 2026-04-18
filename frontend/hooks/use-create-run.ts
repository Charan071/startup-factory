"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";

import { createRun } from "@/lib/api";
import { RunRequest } from "@/lib/types";

export function useCreateRun() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: RunRequest) => createRun(payload),
    onSuccess: (result) => {
      void queryClient.invalidateQueries({ queryKey: ["runs"] });
      if (result.saved_run?.run_id) {
        void queryClient.invalidateQueries({
          queryKey: ["run", result.saved_run.run_id],
        });
      }
    },
  });
}
