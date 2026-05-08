from pathlib import Path


def test_docs_reference_v0_commands_and_pro_checkpoints() -> None:
    readme = Path("README.md").read_text()
    agents = Path("AGENTS.md").read_text()
    roadmap = Path("CURRENT_REALISTIC_ROADMAP.md").read_text()

    assert "eternity validate experiments/examples/linear_ito_toy.yaml" in readme
    assert "eternity run experiments/examples/linear_ito_toy.yaml" in readme
    assert "eternity validate-registry lab_data/registry.yaml" in readme
    assert "eternity hash-artifact lab_data/raw/synthetic_v0/transmission_fixture.csv" in readme
    assert "Pro checkpoint recommended" in agents
    assert "Pro Model Checkpoints" in roadmap
    assert "Project Atlas Maintenance Rule" in agents


def test_project_atlas_entrypoints_and_required_sections_exist() -> None:
    readme = Path("README.md").read_text()
    atlas_markdown = Path("docs/PROJECT_ATLAS.md")
    atlas_html = Path("docs/project_atlas/index.html")
    atlas_css = Path("docs/project_atlas/assets/atlas.css")
    atlas_js = Path("docs/project_atlas/assets/atlas.js")
    netlify_config = Path("netlify.toml")

    assert atlas_markdown.exists()
    assert atlas_html.exists()
    assert atlas_css.exists()
    assert atlas_js.exists()
    assert netlify_config.exists()
    assert "docs/PROJECT_ATLAS.md" in readme
    assert 'publish = "docs/project_atlas"' in netlify_config.read_text()

    html = atlas_html.read_text()
    required_section_ids = [
        "home",
        "simple-roadmap",
        "authority-map",
        "storyboard",
        "promotion-conveyor",
        "reverse-goal-maps",
        "multiple-path-map",
        "conflict-board",
        "evidence-ladder",
        "roadmap-swimlanes",
        "node-template",
    ]
    for section_id in required_section_ids:
        assert f'id="{section_id}"' in html

    markdown = atlas_markdown.read_text()
    assert "First calibrated linear ENZ digital twin checkpoint" in html
    assert "calibrated_linear_evidence" in html
    assert "holdout measurement" in html
    assert 'class="reverse-map compact atlas-node"' in html
    assert 'class="map-root' in html
    assert 'class="map-node complete"' in html
    assert 'class="map-node in-progress"' in html
    assert 'class="map-node not-started"' in html
    assert 'class="map-node blocked"' in html
    assert "Simple Roadmap" in markdown
    assert "calibrated_linear_evidence" in markdown
    assert "left-to-right branching map" in markdown

    atlas_text = "\n".join(
        path.read_text() for path in [atlas_markdown, atlas_html, atlas_css, atlas_js]
    )
    assert "TODO" not in atlas_text
    assert "TBD" not in atlas_text
