from pathlib import Path


def test_plan_and_issue_docs_exist():
    assert Path("docs/plans/index.md").exists()
    assert Path("docs/plans/2026-04-17-startup-factory-v1.md").exists()
    assert Path("issues/index.md").exists()
    assert Path("issues/ISSUE-001-startup-factory-mvp.md").exists()


def test_readme_links_to_plan_and_issues():
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/plans/2026-04-17-startup-factory-v1.md" in readme
    assert "docs/plans/index.md" in readme
    assert "issues/index.md" in readme


def test_no_legacy_status_folder_or_reference_exists():
    legacy_folder = Path("docs") / ("week" + "ly")
    assert not legacy_folder.exists()

    markdown_paths = [Path("README.md")]
    markdown_paths.extend(Path("docs").rglob("*.md"))
    markdown_paths.extend(Path("issues").rglob("*.md"))

    for path in markdown_paths:
        text = path.read_text(encoding="utf-8").lower()
        assert "legacy recurring-status folder" not in text
