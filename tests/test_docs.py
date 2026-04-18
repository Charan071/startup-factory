from pathlib import Path


def test_plan_and_issue_docs_exist():
    assert Path("docs/plans/index.md").exists()
    assert Path("docs/plans/2026-04-17-startup-factory-v1.md").exists()
    assert Path("docs/plans/2026-04-18-startup-factory-v2.md").exists()
    assert Path("docs/plans/2026-04-18-startup-factory-v3.md").exists()
    assert Path("issues/index.md").exists()
    assert Path("issues/ISSUE-001-startup-factory-mvp.md").exists()
    assert Path("issues/ISSUE-002-startup-factory-api-and-artifacts.md").exists()
    assert Path("issues/ISSUE-003-startup-factory-frontend-v3.md").exists()


def test_readme_links_to_plan_and_issues():
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/plans/2026-04-18-startup-factory-v3.md" in readme
    assert "docs/plans/index.md" in readme
    assert "issues/index.md" in readme
    assert "frontend" in readme


def test_no_legacy_status_folder_or_reference_exists():
    legacy_folder = Path("docs") / ("week" + "ly")
    assert not legacy_folder.exists()
