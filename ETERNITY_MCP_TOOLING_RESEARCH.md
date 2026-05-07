# Eternity MCP And Connector Tooling Research

Date: 2026-05-07

## Context

Eternity is currently a roadmap-only repo for a long-horizon AI researcher around ultrafast optics and ENZ material physics. The first build target in `DAY_1_FUTURE_ROADMAP.md` is infrastructure: structured experiment specs, a lab-data registry, Drude/Drude-Lorentz fitting, transfer-matrix simulation, reproducible runs, reports, and tests. Tooling should therefore prioritize reproducibility, literature traceability, local data provenance, and controlled execution before autonomous lab control.

## Installed Or Visible In This Codex Session

| Tool or connector | Status here | Relevance to Eternity |
| --- | --- | --- |
| Consensus connector | Callable after discovery | Strong immediate literature search. It advertises coverage across Semantic Scholar, PubMed, Scopus, and arXiv. Good first-line search before dedicated MCP installs. |
| GitHub connector | Callable after discovery | Useful once Eternity is published or connected to GitHub: repo search, PRs, issues, review flow. Local `git`/shell is enough before publishing. |
| Google Drive connector | Callable after discovery | Useful for lab notes, shared Docs/Sheets/Slides, exported reports, and lecture/thesis/paper materials. |
| Gmail connector | Callable after discovery | Useful later for finding paper correspondence, collaborator threads, attachments, and meeting context. Treat as sensitive. |
| Google Calendar connector | Callable after discovery | Useful later for experiment scheduling and lab planning, not for V0 simulation infrastructure. |
| Hugging Face connector | Callable after discovery | Useful for ML papers, datasets/models, Spaces, and remote CPU/GPU jobs in Docker containers. Later useful for surrogates or ML workflows. |
| Node REPL MCP | Callable | Useful for quick JS-side scripts, but not central for the Python-heavy physics stack. |
| Local shell/Python | Available through Codex command execution | Must-have now for repo work, tests, simulations, plotting, data hashing, and reproducibility. |
| OpenAI developer docs MCP | Enabled in local Codex MCP config | Relevant only when building with OpenAI APIs, ChatGPT Apps SDK, or Codex docs. Keep enabled. |
| xcodebuildmcp | Enabled in local Codex MCP config | Not relevant to Eternity unless a native Apple app appears later. |
| Disabled local MCP entries | Present but disabled: chrome-devtools, context7, markitdown, plasmate, proxyman, serena, XcodeBuildMCP duplicate | Low priority for Eternity right now. `markitdown` could become useful for PDF/doc conversion later; `serena` could help broad codebase navigation once the repo is larger. |
| Slack | Not callable in this session | Useful later only if lab/collaborator communication actually happens in Slack. |

## Must-Have Now

### 1. Filesystem And Local Data Registry

Use a filesystem MCP or native Codex filesystem access for tightly scoped local directories. The reference MCP servers list includes `Filesystem`, `Git`, `Memory`, `PostgreSQL`, `SQLite`, `Google Drive`, and `Slack` style servers. The filesystem server is the right pattern for an agent that needs controlled access to `lab_data/`, `experiments/`, `results/`, and `reports/`.

Recommendation:

- Start with repo-local structured files, not a remote database.
- Use YAML for experiment specs, CSV/Parquet/HDF5 for measurements, JSON sidecars for metadata and hashes.
- Add a manifest/registry layer before adding a vector database.
- Use explicit allowlisted directories if installing a filesystem MCP.

Sources:

- Reference MCP servers: https://github.com/modelcontextprotocol/servers

### 2. Literature Search: Consensus First, Dedicated APIs Second

The installed Consensus connector is the fastest immediate path because it already exposes one search surface over Semantic Scholar, PubMed, Scopus, and arXiv. For serious long-term use, add direct source-specific integrations so the system can store exact query strings, returned IDs, abstracts, citation graph metadata, and retrieval timestamps.

Recommended order:

1. Use installed Consensus now for rapid paper discovery.
2. Use the official APIs directly in the Eternity codebase for reproducible ingestion.
3. Add MCP wrappers only when they improve workflow ergonomics.

External options:

- arXiv official API: https://info.arxiv.org/help/api/user-manual.html
- arXiv MCP server: https://github.com/blazickjp/arxiv-mcp-server
- NCBI/PubMed E-utilities: https://www.ncbi.nlm.nih.gov/home/develop/api/
- PubMed MCP server: https://github.com/Augmented-Nature/PubMed-MCP-Server
- Semantic Scholar Academic Graph API: https://www.semanticscholar.org/product/api
- Semantic Scholar MCP server: https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server
- OpenAlex MCP server: https://mcpservers.org/servers/cyanheads/openalex-mcp-server
- Crossref REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Crossref MCP server: https://github.com/botanicastudios/crossref-mcp

### 3. Zotero

Zotero should be the human-curated research library, not the first ingestion database. It is best for papers the researcher has intentionally accepted into the project memory.

Recommendation:

- Use Zotero for curated collections, PDF annotations, citation export, and paper status.
- Keep raw automated literature search results in the Eternity registry first.
- Sync only promoted papers into Zotero collections such as `ENZ core`, `Hot-electron dynamics`, `Pump-probe methods`, `Material models`, and `Rejected/weak evidence`.

External options:

- Zotero Web API docs: https://www.zotero.org/support/dev/web_api/v3/basics
- Zotero MCP server: https://github.com/kujenga/zotero-mcp

### 4. GitHub

Use local git now. Add GitHub connector/MCP when the repo is remote and needs issues, PRs, release notes, CI, or multi-machine collaboration.

Recommendation:

- Must-have once code exists: GitHub repo, issue labels for `model`, `data`, `experiment-spec`, `literature`, `calibration`, `validation`.
- Use GitHub Actions later for test reproducibility and report artifact generation.

External option:

- Official GitHub MCP server: https://github.com/github/github-mcp-server

## Useful Later

### Jupyter And Notebooks

Jupyter is useful for exploration, fit diagnostics, and interactive plots, but the production path should remain scripted and testable. Treat notebooks as exploratory front-ends over versioned datasets and pure Python modules.

Options:

- Jupyter MCP server: https://www.augmentcode.com/mcp/jupyter-mcp-server
- Jupyter MCP Extended: https://github.com/itisaevalex/jupyter-mcp-extended

Recommendation:

- Useful after V0 functions exist.
- Avoid putting authoritative simulation logic only in notebooks.
- Prefer notebooks that import `eternity` modules and save result artifacts to the registry.

### Python Execution And Sandboxes

Local Python execution is already available and is enough for V0. Sandboxed execution becomes useful when running generated analysis code, untrusted scripts, or dependency-heavy exploratory calculations.

Options:

- Docker code sandbox MCP: https://github.com/Automata-Labs-team/code-sandbox-mcp
- Sandbox MCP: https://github.com/pottekkat/sandbox-mcp

Recommendation:

- Use local `uv`/Python for trusted repo tests.
- Add Docker sandboxing before allowing the AI researcher to execute self-generated code automatically.
- Require timeouts, memory limits, read-only data mounts, and artifact output directories.

### Docker, HPC, And Remote Compute

Docker should arrive before HPC. HPC should be a job-submission adapter around stable scripts, not a chat-controlled shell.

Recommendation:

- Start with Dockerfiles or `uv.lock` for reproducible local runs.
- Add job manifests like `runs/<id>/job.yaml`.
- Later build a Slurm/HPC MCP or CLI wrapper with restricted commands: submit, status, cancel, fetch artifacts.
- The installed Hugging Face jobs connector can be useful for remote CPU/GPU ML or surrogate experiments, but not for lab-calibrated physics simulation until the data packaging is clean.

### Databases And Vector Memory

For V0, SQLite or DuckDB is enough. Postgres is useful when the project gets concurrent users, a web app, or heavier metadata queries. Vector databases are later, after the structured registry exists.

Options:

- Reference PostgreSQL and SQLite MCP servers: https://github.com/modelcontextprotocol/servers
- Qdrant MCP server: https://github.com/qdrant/mcp-server-qdrant
- Chroma MCP server: https://github.com/chroma-core/chroma-mcp
- DuckDB MCP extension/server ecosystem: https://duckdb.org/community_extensions/extensions/duckdb_mcp.html

Recommendation:

- Must-have now: SQLite or DuckDB result index plus file hashes.
- Later: Postgres if a service/UI appears.
- Later: Qdrant/Chroma for semantic retrieval over papers, notes, and experiment records.
- Avoid vector-only memory as the source of truth.

### Google Drive, Gmail, Calendar

These are useful for human workflow integration, not core scientific truth.

Recommendation:

- Google Drive: useful now if lab notes or shared docs already live there.
- Gmail: useful later for collaborator correspondence and finding paper/data attachments.
- Calendar: useful later for experiment scheduling and reminders.
- Keep the canonical experiment records in the repo/data registry, not only in Google Workspace.

External Google Workspace MCP option:

- Google Workspace MCP server: https://github.com/ngs/google-mcp-server

### Slack

Slack is useful only if the lab or collaborators actively use it. It is not needed for solo V0.

Options:

- Slack MCP overview: https://slack.com/help/articles/48855576908307-Guide-to-the-Slack-MCP-server
- Reference/community Slack entries are listed from the MCP server ecosystem: https://github.com/modelcontextprotocol/servers

Recommendation:

- Low priority now.
- Add later for searchable collaborator memory and experiment-discussion capture.
- Use narrow channel scopes and avoid giving write permissions initially.

### Lab Instruments, Serial, DAQ

This is important later, but premature for V0. Instrument MCPs exist in pieces, but the correct Eternity path is probably a custom lab-control MCP/server around the actual equipment, safety rules, and data schema.

Options and building blocks:

- PyVISA for USB/Ethernet/GPIB/RS-232 lab instruments: https://www.pyvisa.org/docs
- Serial MCP server package: https://pypi.org/project/serial-mcp-server/
- Sigrok MCP server for logic analyzers/protocol decoding: https://mcp.so/server/sigrok-mcp-server/KenosInc

Recommendation:

- Avoid direct autonomous instrument control until simulation/data registry is mature.
- First build read-only ingestion: import spectra, delay scans, FROG traces, ellipsometry, and detector calibrations.
- Later expose a small, auditable tool set: list instruments, read status, acquire dataset, save raw file, attach metadata.
- Keep human approval gates for anything that moves stages, changes laser power, opens shutters, or modifies DAQ settings.

## Avoid Or Low Priority

| Tool category | Why low priority now |
| --- | --- |
| Autonomous agent frameworks | The roadmap explicitly says not to implement autonomous agents yet. Build the digital twin and lab memory first. |
| Browser automation MCPs | Useful for web apps and scraping, but not core to V0 physics infrastructure. Use normal APIs for papers. |
| Slack/email write actions | High permission risk and low scientific value at the beginning. Read/search is safer than write/send. |
| Direct lab-control MCPs | High safety and data-integrity risk before there is a validated experiment schema and registry. |
| Vector database first | Semantic memory is useful later, but a vector store cannot replace canonical files, metadata, and hashes. |
| Large remote/HPC automation | Premature until local scripts, result contracts, and reproducibility tests exist. |
| Multiple overlapping literature MCPs | Easy to create duplicate, inconsistent paper records. Pick a source-of-truth ingestion schema first. |

## Security And Governance Notes

MCP servers can expose local files, credentials, email, databases, shell execution, and hardware. For Eternity, the risk is not just privacy; it is also scientific contamination and unsafe lab actions.

Rules for this project:

- Prefer read-only permissions first.
- Install third-party MCPs one at a time.
- Pin versions and record install commands in the repo.
- Give each MCP the narrowest possible directory, token scope, and environment variables.
- Treat paper PDFs and web pages as untrusted input because they can contain prompt-injection text.
- Never let an LLM directly control lasers, shutters, motion stages, high-voltage equipment, or DAQ settings without a separate safety layer and human approval.

Official security guidance:

- MCP security best practices: https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices

## Concrete Stack Recommendation

### Start Now

1. Local filesystem plus repo-owned `lab_data/`, `experiments/`, `results/`, and `reports/`.
2. Local Python with `uv`, tests, plotting, and deterministic scripts.
3. SQLite or DuckDB result registry with data hashes.
4. Consensus connector for immediate literature discovery.
5. Direct official API ingestion for arXiv, Semantic Scholar/OpenAlex, Crossref, and PubMed where needed.
6. Zotero as curated library, not raw search storage.
7. Git/GitHub once the first code scaffold exists.

### Add After V0

1. Jupyter MCP for exploratory notebooks over stable modules.
2. Docker sandbox MCP for generated analysis code.
3. Google Drive integration for shared reports and lab notes.
4. Qdrant or Chroma for semantic search over promoted literature and lab memory.
5. GitHub Actions for reproducible validation runs.

### Add Much Later

1. Slack and Gmail read/search over collaborator memory.
2. Calendar scheduling and experiment reminders.
3. Slurm/HPC job-submission MCP with strict allowlisted commands.
4. Custom PyVISA/serial/DAQ lab MCP with read-only mode first and explicit human gates.

## Bottom Line

The right MCP stack for Eternity is not a huge pile of agents. It is a controlled research operating system:

- Canonical local registry for data and result provenance.
- Literature tools that return stable identifiers and reproducible queries.
- Execution tools that are deterministic, sandboxed, and logged.
- Human-curated Zotero/Drive layers for reading and communication.
- Lab-control tools only after the simulator, data contracts, and safety gates exist.
