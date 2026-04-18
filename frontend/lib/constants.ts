import { ConstraintRow } from "@/components/composer/constraint-builder";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

export const DEFAULT_BRIEF =
  "Find B2B workflow SaaS ideas for mid-market logistics operators where manual back-office coordination causes delayed revenue or margin leakage.";

export const DEFAULT_CONSTRAINTS: ConstraintRow[] = [
  {
    id: "constraint-business-model",
    key: "business_model",
    value: "B2B recurring revenue",
  },
  {
    id: "constraint-team-size",
    key: "team_shape",
    value: "Small team feasible in under 6 months",
  },
];

export const PIPELINE_STAGES = [
  {
    id: "industry-scan",
    label: "Industry scan",
    description: "Find sectors where operational friction is still expensive.",
  },
  {
    id: "problem-mine",
    label: "Problem mine",
    description: "Convert broad inefficiency into narrow buyer-specific pain.",
  },
  {
    id: "generate",
    label: "Generate",
    description: "Draft software wedges that feel buildable and monetizable.",
  },
  {
    id: "critique",
    label: "Critique",
    description: "Attack assumptions before the idea gets to feel comfortable.",
  },
  {
    id: "score",
    label: "Score and rank",
    description: "Normalize urgency, willingness to pay, and feasibility.",
  },
];
