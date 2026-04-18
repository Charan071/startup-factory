export type RunRequest = {
  brief: string;
  constraints?: Record<string, string> | null;
  top_k?: number;
};

export type ScoreBreakdown = {
  urgency: number;
  willingness_to_pay: number;
  feasibility: number;
  defensibility: number;
};

export type StartupIdea = {
  title: string;
  industry: string;
  problem: string;
  solution: string;
  icp: string;
  mvp: string;
  gtm: string;
  critic_summary: string;
  score: number;
  score_breakdown: ScoreBreakdown;
};

export type FinalReport = {
  generated_at: string;
  brief: string;
  top_ideas: StartupIdea[];
};

export type SavedRun = {
  run_id: string;
  artifact_path: string;
  artifact_name?: string | null;
  created_at?: string | null;
};

export type RunExecutionResult = {
  report: FinalReport;
  saved_run?: SavedRun | null;
};

export type RunSummary = {
  run_id: string;
  created_at: string;
  brief: string;
  artifact_name: string;
  top_idea_titles: string[];
  top_score?: number | null;
};

export type RunListResponse = {
  runs: RunSummary[];
};

export type SavedRunRecord = {
  saved_run: SavedRun;
  request: RunRequest;
  report: FinalReport;
};
