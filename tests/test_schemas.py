from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from startup_factory.schemas import FinalReport, RunRequest, ScoreBreakdown, StartupIdea


def test_run_request_rejects_blank_brief():
    with pytest.raises(ValidationError):
        RunRequest(brief="   ")


def test_final_report_schema_accepts_ranked_ideas():
    report = FinalReport(
        generated_at=datetime.now(timezone.utc),
        brief="Find workflow software ideas for logistics operators",
        top_ideas=[
            StartupIdea(
                title="FreightInvoiceOps",
                industry="Logistics",
                problem="Manual invoice reconciliation delays cash collection.",
                solution="Automate invoice matching and discrepancy review.",
                icp="Mid-market freight brokerages",
                mvp="Invoice ingestion, matching, and exception queue",
                gtm="Founder-led outbound to finance leaders",
                critic_summary="Budget owner exists, but integrations are the main risk.",
                score=8.9,
                score_breakdown=ScoreBreakdown(
                    urgency=9,
                    willingness_to_pay=9,
                    feasibility=8,
                    defensibility=8,
                ),
            )
        ],
    )

    assert report.top_ideas[0].title == "FreightInvoiceOps"
    assert report.top_ideas[0].score_breakdown.urgency == 9
