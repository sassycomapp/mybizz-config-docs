---
title: "Gbrain & Graphifyy implementation remediation"
doc-id: "mb-4ad8b2c4"
---
Compliance Remediation Strategy — GBrain and Graphify
Purpose
This plan integrates Graphify with the existing PostgreSQL-backed GBrain installation used by OpenCode.

It is designed to:

verify the current GBrain source configuration;

establish a clean GBrain baseline;

prove whether Graphify closes GBrain’s cross-file code-graph gap;

integrate both systems without merging their databases;

prevent AGENTS.md write collisions;

defer unnecessary global-graph and skillpack work;

verify graph quality, provenance, freshness, and security.

The plan is sequential. Complete and verify each step before starting the next. If a verification fails, return to the originating step, correct the problem, and repeat the verification.

Operating principles
PostgreSQL 16 remains the GBrain database backend.

Hermes and OpenClaw are not required.

GBrain and Graphify remain separate systems.

GBrain owns durable memory, decisions, entities, research, and project history.

Graphify owns repository-local structural relationships.

Git files, tests, explicit user instructions, and validated runtime behaviour are authoritative over both graphs.

Graphify inferred relationships are hypotheses until verified against source files.

No automatic Graphify hook is enabled until the graph passes the value test.

No Graphify data is imported into GBrain’s PostgreSQL schema.

No global cross-project graph is created during this remediation.

Target architecture
text
OpenCode
 ├── GBrain MCP
 │    └── decisions, rationale, facts, entities, history
 ├── Graphify MCP
 │    └── code topology, cross-file relationships, impact paths
 ├── Git and repository files
 │    └── current implementation authority
 └── tests and static analysis
      └── runtime and correctness authority
The systems have separate responsibilities:

text
GBrain:    What do we know, and why?
Graphify:  How is the repository connected?
Git/files: What is currently implemented?
Tests:     Does the implementation work?
Phase A — Establish GBrain baseline
Step 1 — Inspect every GBrain source
Action
Run:

bash
psql "$PGURL" -c "
SELECT
    id,
    path,
    config->>'strategy' AS strategy,
    last_commit
FROM sources
ORDER BY id;
"
Scope
The known code sources are:

text
mb-3-cs-code
mb4ecom-code
mb5pdlf-code
Project-library and documentation sources should not be changed automatically. Their intended strategy may be markdown or auto.

Verification
Confirm:

text
mb-3-cs-code  strategy = code
mb4ecom-code  strategy = code
mb5pdlf-code  strategy = code
For every other source, confirm that the strategy matches its intended content.

Record the complete output in the project reference document.

Do not proceed until every source has an intentional strategy.

Step 2 — Correct incorrectly configured code sources
Perform this step separately for each code source that is missing a strategy or is set to markdown.

Replace <source-id> with the actual source identifier.

Action
bash
psql "$PGURL" -c "
UPDATE sources
SET config = config || '{\"strategy\":\"code\"}'::jsonb
WHERE id = '<source-id>';
"
Clear the stored commit so the source is genuinely rescanned:

bash
psql "$PGURL" -c "
UPDATE sources
SET last_commit = NULL
WHERE id = '<source-id>';
"
Force the code strategy during synchronization:

bash
gbrain sync --source <source-id> --strategy code
Verification
For each corrected source:

bash
gbrain sources status <source-id>
gbrain sync --source <source-id> --strategy code --dry-run
gbrain stats
Confirm:

the source strategy is code;

the expected source files are included;

the sync does not silently fall back to Markdown;

page/chunk counts are plausible;

code files are actually represented.

Do not proceed if the source reports “already up to date” immediately after a strategy correction unless the source was already rescanned and the result is documented.

Step 3 — Confirm and document GBrain search mode
Action
bash
gbrain config get search_mode
Confirm the accepted values:

text
conservative
balanced
tokenmax
If the value is missing or not a deliberate decision, choose the mode explicitly:

bash
gbrain config set search_mode balanced
Use the mode that matches the intended quality/token trade-off. Do not select tokenmax merely because it returns more context.

Verification
Run:

bash
gbrain config get search_mode
Record the selected mode and rationale in gbrain-reference.md:

text
Search mode: balanced
Reason: deliberate quality/token trade-off for the current multi-source corpus.
Decision date: 2026-08-14.
Do not proceed until the mode is both explicit and documented.

Step 4 — Capture a fresh GBrain baseline
Action
Run the full, non-fast health check:

bash
gbrain doctor 2>&1 | tee ~/gbrain-doctor-baseline-2026-08-14.txt
Also capture:

bash
gbrain --version
gbrain stats
gbrain sources list --json
gbrain schema active
Verification
Review and record:

GBrain version;

schema version;

active schema pack;

PostgreSQL backend;

pgvector status;

source count;

source strategies;

page and chunk counts;

embedding coverage;

upgrade warnings;

migration warnings;

dream-cycle warnings;

MCP status.

Treat stale entries in ~/.gbrain/upgrade-errors.jsonl separately from live migration state. Your reference document records that this log can preserve historical warnings after the original problem is resolved.

Do not treat MEMORY_VERBS v1 as active unless the current configuration explicitly enables it. Your reference currently records that it exists but is not enabled.

Record the Voyage embedding decision separately:

text
Voyage embeddings:
Not adopted.
Reason: benefit is unproven against the re-embedding cost for the current corpus size.
Decision date: 2026-08-14.
This is a documentation decision, not a doctor acceptance criterion.

Phase B — Establish Graphify independently
Step 5 — Install Graphify through a controlled environment
Action
Install or verify uv using your existing preferred method.

Then install Graphify:

bash
uv tool install graphifyy
Do not maintain multiple active Graphify installations after verification.

Verification
Confirm the executable:

bash
command -v graphify
readlink -f "$(command -v graphify)"
graphify --version
graphify --help
uv tool list | grep -A3 graphify
Do not use this as the primary provenance test:

bash
python3 -c "import graphify; print(graphify.__file__)"
That may inspect a different Python environment from the one used by the graphify executable.

If an older pip installation shadows the uv installation, remove the old copy only after the uv-managed executable has been confirmed:

bash
python3 -m pip show graphifyy
The final state must have one clearly identified active executable.

Step 6 — Verify Graphify’s OpenCode project installation
Do not assume that --platform opencode is valid together with --project. Inspect the installed command first:

bash
graphify install --help
graphify opencode --help
Use the documented OpenCode-specific form if available:

bash
cd /mnt/c/dev/dev-mb-3-cs/mb-3-cs
graphify opencode install --project
If that command is not supported, use:

bash
graphify install --project
Verification
Search for the project-scoped skill:

bash
find . -path '*graphify*' -type f -name 'SKILL.md' -print
Confirm that:

the skill exists inside the repository;

OpenCode can discover it;

/graphify works from this repository;

the project copy is the one being used.

Do not retire the global installation until all of the following are true:

the project-scoped skill exists;

OpenCode loads it;

/graphify works;

no other required project depends on the global copy.

Step 7 — Record a pre-graph repository baseline
Action
From the target repository:

bash
cd /mnt/c/dev/dev-mb-3-cs/mb-3-cs
git rev-parse HEAD
git status --short
find . -maxdepth 3 -type f | sort > /tmp/mb-3-cs-files-before-graphify.txt
Record:

repository path;

Git commit;

working-tree status;

Graphify version;

Python/uv environment;

intended source directories;

files that must be excluded.

Verification
The working tree must be clean or the existing changes must be documented. A graph generated from undocumented uncommitted changes cannot be compared reliably with later results.

Step 8 — Test Graphify’s PostgreSQL capability safely
This step is optional for the core cross-file test and must not be confused with connecting Graphify to GBrain’s internal database.

Decision
First decide which database Graphify is supposed to inspect:

text
Application database:
potentially useful for model/schema/query relationships.

GBrain internal database:
generally low value for improving application code analysis.
Do not use the GBrain superuser connection string for Graphify testing.

Use a read-only PostgreSQL role scoped to the intended application database and schema.

Action
Inspect the installed syntax:

bash
graphify extract --help
graphify add --help
graphify query --help
Confirm the exact PostgreSQL command and whether the PostgreSQL extra is required:

bash
uv tool install "graphifyy[postgres]"
Do not run an assumed command until --help confirms its syntax.

Verification
Confirm:

the PostgreSQL extra is installed;

the command accepts the intended connection form;

the read-only connection succeeds;

only the intended database/schema is inspected;

no write operation is attempted;

the resulting nodes and edges are understandable.

If PostgreSQL extraction is not required for the initial code-graph test, defer this step. Do not let database introspection delay the core value test.

Phase C — Prove Graphify’s value
Step 9 — Build the initial repository graph
Action
From the target repository:

bash
cd /mnt/c/dev/dev-mb-3-cs/mb-3-cs
graphify .
If the current Graphify version requires an explicit mode or output option, use the syntax shown by:

bash
graphify --help
Do not use deep or inferred extraction for the first adequacy test unless the direct structural graph is insufficient.

Verification
Confirm that Graphify produces the expected output files, such as:

text
graphify-out/graph.json
graphify-out/GRAPH_REPORT.md
graphify-out/graph.html
The exact filenames may vary by version.

Inspect the output:

bash
find graphify-out -maxdepth 2 -type f -print
Record:

graph generation time;

source commit;

node count;

edge count;

extracted/inferred/ambiguous counts;

warnings;

skipped files;

output size.

Do not proceed if the graph is empty, contains only documentation, or omits the application code.

Step 10 — Prove the cross-file value proposition
Action
Use the known symbol pair:

bash
graphify path "get_vault_secret" "encrypt"
First confirm the syntax:

bash
graphify path --help
If the command returns JSON or another machine-readable format, preserve that output:

bash
graphify path "get_vault_secret" "encrypt" > /tmp/graphify-vault-encrypt-path.txt
Verification
The test passes only if all conditions are satisfied:

get_vault_secret and encrypt are identified unambiguously.

The path crosses files or modules.

The relevant relationship is marked EXTRACTED.

The result agrees with direct source inspection.

The result is reproducible after a graph rebuild.

The graph source commit matches the repository commit.

The result is not merely an INFERRED path.

The path is not produced only because both symbols appear in the same document.

Record the evidence:

text
Source symbol: get_vault_secret
Source file: <path>
Target symbol: encrypt
Target file: <path>
Relationship: <relationship>
Confidence: EXTRACTED
Repository commit: <hash>
Verified against source: yes
Failure gate
If the path:

fails to resolve;

crosses files but is only INFERRED;

is ambiguous;

disagrees with the source;

changes unpredictably after rebuild;

stop the remediation.

Do not continue to hooks, MCP integration, or broad adoption until the gap is reassessed.

Step 11 — Test additional graph adequacy
The single symbol pair is necessary but insufficient. Test a small manually verified fixture containing:

a cross-file import;

an aliased import;

a relative import;

a function call;

class inheritance;

a re-export;

a configuration reference;

a shell script invoking Python;

an Anvil or framework-specific event path where applicable.

For each relationship, record:

text
expected edge
Graphify result
confidence
source evidence
pass/fail
Use these question categories:

text
What calls this function?
What does this function call?
Which modules depend on this interface?
What is the path from the UI event to server code?
Which files are affected by changing this configuration?
Which migration relates to this model?
Graphify passes the adequacy gate only if it reliably improves the specific cross-file cases that GBrain currently misses.

Phase D — Configure graph scope and provenance
Step 12 — Create controlled ignore rules
Action
Create .graphifyignore in the repository root:

text
node_modules/
.venv/
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
build/
coverage/
graphify-out/cache/
*.pyc
*.generated.py
.env
.env.*
*.pem
*.key
secrets/
credentials/
Review each entry before committing. Do not exclude generated files that are required to understand the runtime system.

Verification
Rebuild or update the graph:

bash
graphify . --update
Inspect the graph structure:

bash
jq 'keys' graphify-out/graph.json
Then verify that excluded paths are absent:

bash
jq -r '.nodes[]?.path // empty' graphify-out/graph.json \
  | grep -E 'node_modules|\.venv|generated\.py|\.env' \
  && echo "Unexpected excluded path found"
Verify that required source paths are present:

bash
jq -r '.nodes[]?.path // empty' graphify-out/graph.json \
  | grep -E 'server_code|client_code|tests'
Adjust the ignore rules if essential application files are missing.

Step 13 — Record graph provenance
The graph must identify the repository state from which it was generated.

Action
Record in the project reference document:

text
Graphify:
- Version: <graphify version>
- Package: graphifyy
- Repository: /mnt/c/dev/dev-mb-3-cs/mb-3-cs
- Source commit: <git hash>
- Generated: <timestamp>
- Graph output: <path>
- Extraction mode: <mode>
- Included file classes: <list>
- Excluded paths: <list>
- Known limitations: <list>
If the generated graph does not contain the source commit internally, maintain this metadata beside the graph.

Verification
After changing one source file:

record the old commit;

update the graph;

confirm the graph timestamp or metadata changes;

confirm the changed symbol is reflected;

confirm the graph does not claim to represent the old commit.

Do not let OpenCode query a graph whose provenance does not match the current checkout.

Phase E — Integrate with OpenCode
Step 14 — Integrate Graphify MCP only after the value test
Action
Use Graphify’s documented MCP configuration for OpenCode after confirming the installed version’s syntax.

Graphify’s MCP interface exposes graph tools such as:

text
query_graph
shortest_path
get_node
get_neighbors
graph_stats
triage_prs
Keep GBrain MCP and Graphify MCP as separate servers.

Verification
In OpenCode, confirm that both tool groups are visible and distinguishable.

Test:

text
Graphify:
show the path from get_vault_secret to encrypt

GBrain:
what prior decisions and incidents relate to vault secret handling?
Confirm that:

the first request uses Graphify;

the second request uses GBrain;

neither server is queried unnecessarily;

the agent can read the current source files after retrieval.

Step 15 — Establish explicit routing policy
Add the following policy to the project’s agent instructions:

text
## Knowledge and code graph policy

For unfamiliar code:
1. Query Graphify for current structural relationships, callers, callees, paths, and impact.
2. Query GBrain for decisions, rationale, history, prior incidents, research, and benchmarks.
3. Read the current repository files before changing code.
4. Treat Git files, explicit user instructions, tests, and validated runtime behaviour as authoritative.
5. Treat Graphify INFERRED and AMBIGUOUS edges as hypotheses.
6. Treat GBrain memory as advisory when it conflicts with current files.
7. Verify graph provenance against the current Git commit.
8. After a successful change, write important decisions and results back to GBrain.
Verification
Run representative prompts and confirm the routing behaviour. Do not rely only on the presence of the text in AGENTS.md.

Phase F — Resolve AGENTS.md ownership
Step 16 — Back up and inspect existing instructions
Action
bash
cd /mnt/c/dev/dev-mb-3-cs/mb-3-cs
cp AGENTS.md "AGENTS.md.backup-$(date +%Y%m%d-%H%M%S)"
sha256sum AGENTS.md
Inspect existing GBrain and Graphify sections:

bash
grep -n -i -E 'gbrain|graphify|sync-gbrain|graph memory' AGENTS.md
Step 17 — Create one bounded managed section
Use exactly one managed block:

text
<!-- BEGIN GRAPH MEMORY GUIDANCE -->
## Knowledge and code graph policy

1. Query Graphify for current structural relationships.
2. Query GBrain for decisions, rationale, history, and prior incidents.
3. Read current source files before changing code.
4. Treat Git files and tests as authoritative over either graph.
5. Treat Graphify INFERRED and AMBIGUOUS edges as hypotheses.
6. Verify graph provenance against the current Git commit.
7. After a successful change, write important decisions and results to GBrain.

<!-- END GRAPH MEMORY GUIDANCE -->
Do not allow two independent tools to own the whole file.

Verification
Run:

bash
test "$(grep -c '<!-- BEGIN GRAPH MEMORY GUIDANCE -->' AGENTS.md)" -eq 1
test "$(grep -c '<!-- END GRAPH MEMORY GUIDANCE -->' AGENTS.md)" -eq 1
sed -n '/BEGIN GRAPH MEMORY GUIDANCE/,/END GRAPH MEMORY GUIDANCE/p' AGENTS.md
Then run the GBrain sync and Graphify project registration separately.

After each operation, verify:

bash
test "$(grep -c '<!-- BEGIN GRAPH MEMORY GUIDANCE -->' AGENTS.md)" -eq 1
test "$(grep -c '<!-- END GRAPH MEMORY GUIDANCE -->' AGENTS.md)" -eq 1
Also confirm that the content outside the managed block was preserved. Markers alone do not prove that another tool did not overwrite unrelated instructions.

The final state must have:

text
one opening marker;
one closing marker;
one complete policy block;
no duplicate Graphify/GBrain policy;
pre-existing AGENTS.md content preserved;
one designated writer for the managed block.
Phase G — Decide on graph artifacts and hooks
Step 18 — Decide which Graphify artifacts belong in Git
Inspect the outputs before changing .gitignore:

bash
du -ah graphify-out | sort -h
git status --short
Review for:

secrets;

absolute local paths;

embedded document content;

credentials;

excessive size;

unstable generated data.

A reasonable initial policy is:

text
graphify-out/cache/
graphify-out/cost.json
Commit only the artifacts that are useful and safe:

text
graph.json
GRAPH_REPORT.md
Keep graph.html local unless it is small, safe, and useful to the project.

Verification
Confirm:

bash
git status --short
git check-ignore -v graphify-out/cost.json
git ls-files graphify-out/graph.json graphify-out/GRAPH_REPORT.md
Do not commit graph artifacts until provenance and sensitivity checks pass.

Step 19 — Defer Git hooks until graph adequacy is proven
Do not install the hook before the cross-file value proposition and graph-quality tests pass.

After the graph has passed those tests, inspect the hook command:

bash
graphify hook --help
Install only if the behaviour is understood:

bash
graphify hook install
Verification
bash
graphify hook status
git config --local --list | grep -i graph
cat .git/hooks/post-commit 2>/dev/null
cat .git/hooks/post-merge 2>/dev/null
Confirm:

existing Git hooks were preserved;

the Graphify hook is present;

the hook updates the intended graph;

the hook does not write to GBrain;

the hook does not overwrite AGENTS.md;

the hook does not expose secrets;

the update completes within an acceptable time.

If automatic rebuilding is slow or unreliable, remove the hook and use a controlled manual or CI update.

Phase H — Optional GBrain skillpack work
Step 20 — Decide separately whether to scaffold GBrain skills
This is not required to prove Graphify’s value.

If you choose to evaluate the skillpack in the documentation repository:

bash
cd /mnt/c/dev/dev-mb-3-cs/makepdlf-project-library
gbrain skillpack scaffold --all
Use the exact workspace/path form supported by the installed version.

Verification
bash
find skills -name SKILL.md -type f | sort
test -f skills/RESOLVER.md
grep -R '^triggers:' skills/*/SKILL.md
Compare the scaffolded skills with the bundled manifest or resolver. Do not assume --all includes every skill referenced by the resolver; the upstream repository has an open issue documenting such a mismatch.

Treat this as an OpenCode skillpack evaluation, not as a Hermes/OpenClaw installation step.

Phase I — Keep the global graph deferred
Step 21 — Do not build the global cross-project graph yet
Do not combine:

text
mb-3-cs
mb4ecom
mb5pdlf
project-library
into one Graphify graph at this stage.

Reasons:

mb4ecom and mb5pdlf currently contain too little real code for meaningful benefit;

cross-project symbol collisions become harder to interpret;

graph queries become noisier;

source ownership becomes ambiguous;

freshness management becomes more complex;

project-specific agent instructions can become contaminated.

Record the decision:

text
Global Graphify graph:
Deferred.

Reason:
The smaller projects do not yet contain enough real code to justify a
cross-project graph. The current remediation focuses on proving value in
mb-3-cs first.

Review condition:
Reassess when mb4ecom and mb5pdlf contain substantial active code or when
a cross-project dependency question becomes a real requirement.
Final verification
Run the final checks only after all preceding steps have passed.

GBrain
bash
gbrain doctor
gbrain --version
gbrain stats
gbrain sources list --json
gbrain schema active
Confirm:

all code sources explicitly use code;

intended Markdown sources remain correctly configured;

no unexplained sync failures remain;

embedding coverage is documented;

active schema pack is correct;

live migration state is understood;

stale historical warnings are separated from live failures.

Graphify
bash
graphify --version
graphify hook status
find graphify-out -maxdepth 2 -type f -print
Confirm:

one active Graphify executable;

correct project-scoped skill;

graph output exists;

graph source commit matches the repository;

required code is present;

excluded paths are absent;

the tested cross-file path is EXTRACTED;

graph output contains no secrets.

OpenCode integration
bash
test "$(grep -c '<!-- BEGIN GRAPH MEMORY GUIDANCE -->' AGENTS.md)" -eq 1
test "$(grep -c '<!-- END GRAPH MEMORY GUIDANCE -->' AGENTS.md)" -eq 1
git status --short
Confirm:

one complete managed policy block;

no duplicated instructions;

no unrelated AGENTS.md content was lost;

both MCP servers are available;

Graphify handles structural questions;

GBrain handles historical and semantic questions.

Completion criteria
The remediation is complete only when all of the following are true:

Every code-type GBrain source has an explicit code strategy.

Each corrected source has been genuinely rescanned.

A fresh GBrain health baseline is recorded.

Search mode is explicit and documented.

Graphify has one verified active installation.

Graphify is available to the target OpenCode project.

The graph contains the required application code.

The tested cross-file path is resolved and marked EXTRACTED.

Graph output is reproducible and tied to a Git commit.

Ignore rules exclude sensitive and irrelevant material without excluding required code.

GBrain and Graphify remain separate systems.

OpenCode routes structural questions to Graphify.

OpenCode routes rationale and history questions to GBrain.

AGENTS.md has one intact managed policy block.

Git hooks are enabled only if their behaviour is understood and acceptable.

No Hermes or OpenClaw component is required.

The global cross-project graph remains explicitly deferred.

Optional GBrain skillpack work is verified separately from Graphify remediation.

Final decision rule
Adopt Graphify for the OpenCode project only if it demonstrably improves the known GBrain weakness:

text
GBrain:
same-file or unresolved cross-file code relationships

Graphify:
reproducible, source-verified, EXTRACTED cross-file relationships
If Graphify does not meet that test, stop before MCP integration and hooks. Continue using GBrain for durable memory, and reassess Graphify’s parser, configuration, or version separately.