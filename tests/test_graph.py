from startup_factory.graph import run_startup_factory
from startup_factory.schemas import RunRequest


class FakeLLM:
    def __init__(self, payloads):
        self.payloads = list(payloads)

    def generate_structured(self, *, output_model, **_kwargs):
        payload = self.payloads.pop(0)
        return output_model.model_validate(payload)


def make_payloads():
    return [
        {
            "industries": [
                {
                    "name": "Logistics",
                    "inefficiency": "Finance teams still reconcile invoices manually.",
                    "why_now": "Margin pressure makes back-office automation easier to justify.",
                },
                {
                    "name": "Specialty Clinics",
                    "inefficiency": "Referral leakage and scheduling handoffs are still manual.",
                    "why_now": "Staff shortages are raising the cost of coordination.",
                },
            ]
        },
        {
            "problems": [
                {
                    "id": "problem_1",
                    "industry": "Logistics",
                    "problem": "Manual freight invoice reconciliation slows collections.",
                    "buyer_role": "VP Finance",
                    "pain_summary": "Teams lose hours each week matching invoices to load records.",
                },
                {
                    "id": "problem_2",
                    "industry": "Specialty Clinics",
                    "problem": "Referral handoffs stall because staff chase paperwork manually.",
                    "buyer_role": "Clinic Operations Director",
                    "pain_summary": "Unscheduled referrals reduce visit volume and clinician utilization.",
                },
            ]
        },
        {
            "ideas": [
                {
                    "id": "problem_1_idea",
                    "title": "FreightInvoiceOps",
                    "industry": "Logistics",
                    "problem": "Manual freight invoice reconciliation slows collections.",
                    "solution": "Automate invoice matching, discrepancy detection, and approval routing.",
                    "icp": "Mid-market freight brokers",
                    "mvp": "Invoice ingestion, load matching, and exception queue",
                    "gtm": "Founder-led outbound to finance leaders",
                },
                {
                    "id": "problem_2_idea",
                    "title": "ReferralFlow",
                    "industry": "Specialty Clinics",
                    "problem": "Referral handoffs stall because staff chase paperwork manually.",
                    "solution": "Track referrals, missing paperwork, and scheduling readiness in one workflow.",
                    "icp": "Multi-location specialty clinics",
                    "mvp": "Referral inbox, status tracking, and task routing",
                    "gtm": "Channel partnerships with specialty clinic consultants",
                },
            ]
        },
        {
            "critiques": [
                {
                    "idea_id": "problem_1_idea",
                    "critic_summary": "Strong finance pain, but integrations will determine adoption speed.",
                    "fatal_risks": ["ERP integration complexity"],
                    "strengths": ["Clear buyer", "Recurring workflow"],
                },
                {
                    "idea_id": "problem_2_idea",
                    "critic_summary": "Useful workflow, but buying urgency may vary by clinic size.",
                    "fatal_risks": ["Can look like lightweight task software"],
                    "strengths": ["Operational pain is easy to explain"],
                },
            ]
        },
        {
            "scores": [
                {
                    "idea_id": "problem_1_idea",
                    "urgency": 9,
                    "willingness_to_pay": 9,
                    "feasibility": 8,
                    "defensibility": 7,
                    "overall": 8.8,
                    "reasoning": "Clear finance pain with budget owner and repeatable workflow.",
                },
                {
                    "idea_id": "problem_2_idea",
                    "urgency": 7,
                    "willingness_to_pay": 7,
                    "feasibility": 8,
                    "defensibility": 6,
                    "overall": 7.1,
                    "reasoning": "Operationally useful but weaker moat and inconsistent urgency.",
                },
            ]
        },
    ]


def test_graph_smoke_run_returns_ranked_report():
    report = run_startup_factory(
        RunRequest(
            brief="Find vertical SaaS ideas for operational bottlenecks.",
            top_k=2,
        ),
        llm=FakeLLM(make_payloads()),
    )

    assert len(report.top_ideas) == 2
    assert report.top_ideas[0].title == "FreightInvoiceOps"
    assert report.top_ideas[0].score >= report.top_ideas[1].score


def test_top_k_truncates_ranked_ideas():
    report = run_startup_factory(
        RunRequest(
            brief="Find vertical SaaS ideas for operational bottlenecks.",
            top_k=1,
        ),
        llm=FakeLLM(make_payloads()),
    )

    assert len(report.top_ideas) == 1
    assert report.top_ideas[0].title == "FreightInvoiceOps"
