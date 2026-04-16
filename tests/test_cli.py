from datetime import datetime, timezone

from startup_factory.cli import main
from startup_factory.schemas import FinalReport, ScoreBreakdown, StartupIdea


def make_report():
    return FinalReport(
        generated_at=datetime.now(timezone.utc),
        brief="Find vertical SaaS ideas in logistics.",
        top_ideas=[
            StartupIdea(
                title="FreightInvoiceOps",
                industry="Logistics",
                problem="Manual invoice reconciliation slows collections.",
                solution="Automate invoice matching and approval routing.",
                icp="Mid-market freight brokerages",
                mvp="Invoice ingestion and discrepancy queue",
                gtm="Outbound to finance leaders",
                critic_summary="High pain, but integration depth matters.",
                score=8.8,
                score_breakdown=ScoreBreakdown(
                    urgency=9,
                    willingness_to_pay=9,
                    feasibility=8,
                    defensibility=7,
                ),
            )
        ],
    )


def test_cli_markdown_output(monkeypatch, capsys):
    monkeypatch.setattr("startup_factory.cli.run_startup_factory", lambda _request: make_report())

    exit_code = main(["--brief", "Find vertical SaaS ideas in logistics."])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "# Startup Factory Report" in captured.out
    assert "FreightInvoiceOps" in captured.out


def test_cli_json_output(monkeypatch, capsys):
    monkeypatch.setattr("startup_factory.cli.run_startup_factory", lambda _request: make_report())

    exit_code = main(
        ["--brief", "Find vertical SaaS ideas in logistics.", "--json"]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"brief": "Find vertical SaaS ideas in logistics."' in captured.out
    assert '"title": "FreightInvoiceOps"' in captured.out
