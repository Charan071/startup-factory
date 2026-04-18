import { API_BASE_URL } from "./constants";
import {
  RunExecutionResult,
  RunListResponse,
  RunRequest,
  SavedRunRecord,
} from "./types";

class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) {
        message = payload.detail;
      }
    } catch {
      message = response.statusText || message;
    }

    throw new ApiError(message, response.status);
  }

  return (await response.json()) as T;
}

export function createRun(payload: RunRequest) {
  return fetchJson<RunExecutionResult>("/runs", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getRuns(limit = 20) {
  return fetchJson<RunListResponse>(`/runs?limit=${limit}`);
}

export function getRun(runId: string) {
  return fetchJson<SavedRunRecord>(`/runs/${runId}`);
}
