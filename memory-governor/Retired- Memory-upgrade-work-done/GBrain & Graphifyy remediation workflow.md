---
title: "GBrain & Graphifyy remediation workflow"
doc-id: "mb-3937f5bc"
---
This is an appropriate task for OpenCode, but it must be executed as a controlled sequence of small, verified work packages, not as one large autonomous prompt.

DeepSeek V4 Pro should be adequate for most of the work, including inspection, SQL diagnosis, documentation, Graphify configuration, and ordinary OpenCode orchestration. I would not give it unrestricted authority over database updates, Git hooks, AGENTS.md, or model-dependent GBrain operations. Use explicit approval gates and require verification after every state-changing action.

The latest DeepSeek V4 Pro release supports tool use, structured output, and high/max reasoning modes; published benchmark claims place it near frontier coding performance, although those figures are not a guarantee for your specific WSL/OpenCode workflow.

Recommended model policy
Use DeepSeek V4 Pro as the primary implementation and verification model, with reasoning set to high rather than maximum for routine work.

Work	Model recommendation
Read-only inspection	DeepSeek V4 Pro, normal or high reasoning
SQL inspection and report generation	DeepSeek V4 Pro, high reasoning
GBrain source-strategy remediation	DeepSeek V4 Pro, high reasoning, human approval
Graphify installation checks	DeepSeek V4 Pro, normal/high reasoning
Graphify graph build and query	DeepSeek V4 Pro, high reasoning
AGENTS.md policy editing	DeepSeek V4 Pro, high reasoning, manual diff review
Git hook installation	DeepSeek V4 Pro, high/max reasoning, explicit approval
PostgreSQL schema changes	DeepSeek V4 Pro may prepare SQL, but you approve and execute
GBrain dream-cycle interpretation	DeepSeek V4 Pro can inspect results, but do not assume it validates model failures
Final acceptance review	DeepSeek V4 Pro high reasoning plus your review
Ambiguous or destructive change	Use Anthropic selectively or stop for your approval
DeepSeek is adequate as the operator, but it should not be the sole source of truth. The actual verification must come from:

text
psql output
GBrain output
Graphify output
Git diff
source files
tests
Do not use Anthropic continuously
You do not need to use the Anthropic API for the entire task. That would be unnecessarily expensive.

Use DeepSeek for:

planning;

command selection;

reading documentation;

interpreting SQL output;

comparing Graphify and GBrain results;

drafting Markdown;

writing controlled scripts;

reviewing diffs;

preparing verification reports.

Use your Anthropic key only as a selective escalation mechanism, for example:

DeepSeek produces an ambiguous interpretation of a migration or schema issue.

The agent proposes a destructive database change.

Graphify and GBrain produce conflicting architecture conclusions.

A final independent review is needed for a high-risk change.

A model-dependent GBrain dream phase requires Anthropic specifically.

For normal GBrain retrieval and Graphify code analysis, Anthropic should not be required. Your existing local reference specifically identifies Anthropic as a dependency for some GBrain intelligence phases, especially extract_atoms; that is separate from using Anthropic as the OpenCode orchestration model.

The distinction is important:

text
OpenCode model:
the model directing the work.

GBrain dream provider:
the model used by specific GBrain phases.

Graphify parser:
the local structural graph extractor.
Changing the OpenCode model does not automatically replace the provider used internally by GBrain’s dream cycle.

Use OpenCode in increments
Do not paste the whole plan as one instruction and ask OpenCode to execute it. Give OpenCode one work package at a time.

Each work package should contain:

text
objective
allowed scope
forbidden actions
commands or inspection requirements
verification criteria
required report
stop condition
The agent should not continue automatically after a failed verification.

# Work package 1 — Read-only baseline
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---

text
You are performing a read-only baseline inspection.

Do not modify files, databases, Git hooks, agent instructions, package installations, or Graphify configuration.

Inspect:
1. The current Git status and commit for mb-3-cs.
2. The GBrain version, schema, active schema pack, statistics, and all source strategies.
3. The installed Graphify executable, version, help output, and installation path.
4. Existing AGENTS.md sections mentioning GBrain or Graphify.
5. Existing Graphify output and ignore files, if present.

Use read-only commands only.

Return:
- exact commands run;
- complete relevant outputs;
- anomalies;
- unknowns;
- recommended next work package.

Stop after reporting. Do not fix anything.
This is the first gate. Review the output before allowing modifications.

# Work package 2 — GBrain source audit
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



text
Audit the GBrain source configuration.

Do not modify the database yet.

Query every source with:
- id;
- path;
- config strategy;
- last_commit.

Classify each source as:
- code source;
- Markdown/project-library source;
- mixed or uncertain.

For code sources, identify any source whose strategy is missing or not code.

Return:
- SQL output;
- source classification;
- proposed corrections;
- expected verification for each correction.

Stop. Do not execute UPDATE statements or synchronization.
You remain the approval gate for the SQL updates.

# Work package 3 — Correct GBrain code sources
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



Only after reviewing Work Package 2:

text
Correct only the explicitly approved GBrain code sources.

For each approved source:
1. Add config.strategy = code.
2. Clear last_commit so the source is genuinely rescanned.
3. Show the SQL statements before executing them.
4. Execute the approved update.
5. Run a dry-run or source status check.
6. Synchronize using the code strategy.
7. Report page/chunk changes and any warnings.

Do not modify non-code sources.
Do not change the schema.
Do not run dream.
Do not change embeddings.
Stop if the result is unexpected.
DeepSeek is suitable for preparing and interpreting this work, but you should approve the actual UPDATE statements.

# Work package 4 — GBrain baseline and search mode
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



text
Establish the post-source-correction GBrain baseline.

Run:
- gbrain doctor;
- gbrain stats;
- gbrain sources list --json;
- gbrain schema active;
- gbrain --version;
- gbrain config get search_mode.

Do not change search_mode automatically.

If the value is absent or not documented as deliberate, propose a mode and explain the trade-off. Do not set it until approved.

Capture the full baseline and update only the agreed reference documentation.
Do not run dream or self-upgrade.
I recommend balanced as the initial documented mode unless your actual query-quality tests support another choice.

# Work package 5 — Graphify executable and project installation
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



text
Verify the Graphify installation.

Do not remove the existing pip installation yet.
Do not modify AGENTS.md yet.
Do not install Git hooks yet.

Inspect:
- command -v graphify;
- resolved executable path;
- graphify --version;
- graphify --help;
- uv tool list;
- graphify install --help;
- graphify opencode --help.

Determine the documented project-scoped OpenCode installation command for the installed version.

Return:
- active executable;
- package version;
- installation source;
- exact project-install command;
- possible PATH conflicts.

Stop before installing or removing anything.
After approval:

text
Install Graphify project-scoped for this repository only.

Repository:
 /mnt/c/dev/dev-mb-3-cs/mb-3-cs

Use the exact command established in the previous inspection.

Do not install Git hooks.
Do not edit AGENTS.md manually.
Do not remove the global installation until project discovery is verified.

Verify:
- project-scoped Graphify skill exists;
- OpenCode can discover it;
- /graphify works in this repository.

Stop and report.
# Work package 6 — Graphify initial graph
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



text
Build the initial Graphify graph for mb-3-cs.

Do not connect to GBrain’s PostgreSQL database.
Do not install hooks.
Do not modify AGENTS.md.
Do not commit graph artifacts.

Record:
- Graphify version;
- repository commit;
- graph command;
- output files;
- node count;
- edge count;
- extracted/inferred/ambiguous counts;
- skipped files;
- warnings;
- output size.

Inspect the graph output and report whether application code is present.

Stop after reporting.
# Work package 7 — Cross-file adequacy test
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



text
Test whether Graphify closes the known GBrain cross-file code-graph gap.

Use the real symbol pair:
- get_vault_secret
- encrypt

First inspect the source files and establish that the relationship is cross-file.

Then query Graphify using the installed version's documented path command.

The test passes only if:
1. both symbols resolve;
2. the path crosses files;
3. the relationship is EXTRACTED;
4. the result agrees with direct source inspection;
5. the repository commit matches the graph provenance;
6. the result is reproducible after rebuild.

If the result is unresolved, ambiguous, or only inferred:
- do not continue to hooks or broad integration;
- report the failure;
- identify whether the cause is installation, parser coverage, command usage, or a genuine Graphify limitation.

Stop after the test.
This is the most important gate in the entire project.

# Work package 8 — Graph adequacy fixture
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



text
Evaluate Graphify against a small manually verified fixture.

Test:
- cross-file import;
- aliased import;
- relative import;
- function call;
- class inheritance;
- re-export;
- configuration reference;
- shell-to-Python relationship;
- Anvil/framework-specific relationship where applicable.

For each expected edge, record:
- expected relationship;
- Graphify result;
- confidence;
- source evidence;
- pass/fail.

Do not modify GBrain.
Do not install hooks.
Do not change AGENTS.md.

Return a graph adequacy report and stop.
Do not accept Graphify merely because it resolves one carefully selected path. It must be useful across the patterns that matter in your codebase.

# Work package 9 — Ignore rules and provenance
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



text
Prepare Graphify scope controls.

Before editing:
1. inspect the current repository;
2. identify generated files, caches, secrets, credentials, and required runtime files;
3. propose .graphifyignore entries.

Do not write the file until the proposed exclusions are shown.

After approval:
1. create .graphifyignore;
2. rebuild the graph;
3. verify excluded paths are absent;
4. verify required application paths remain present;
5. record the source Git commit and Graphify version.

Do not install hooks or modify AGENTS.md.

# Work package 10 — MCP integration
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



Only after Graphify passes the adequacy gate:

text
Integrate Graphify MCP with OpenCode.

Do not change GBrain configuration.
Do not modify AGENTS.md yet.
Do not install Git hooks.

Configure Graphify MCP using the installed version's documented OpenCode method.

Verify:
1. Graphify MCP starts;
2. GBrain MCP still starts;
3. both tool sets are visible;
4. structural queries go to Graphify;
5. historical and rationale queries go to GBrain;
6. neither system is queried unnecessarily.

Run only read-only test queries.
Stop and report.

# Work package 11 — AGENTS.md ownership
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



text
Audit AGENTS.md integration ownership.

Do not allow two tools to rewrite the entire file.

Back up AGENTS.md.
Inspect existing GBrain and Graphify instructions.
Propose one bounded managed block using these markers:

<!-- BEGIN GRAPH MEMORY GUIDANCE -->
...
<!-- END GRAPH MEMORY GUIDANCE -->

Show the proposed diff before writing.

The block must state:
- Graphify handles current structural relationships;
- GBrain handles decisions and history;
- source files and tests are authoritative;
- inferred edges require verification;
- graph provenance must match the current commit;
- important completed decisions are written back to GBrain.

Stop before writing the file.
After approval:

text
Apply only the approved bounded AGENTS.md block.

Preserve all unrelated content.
Run the GBrain sync and Graphify registration separately.
After each operation verify:
- one opening marker;
- one closing marker;
- one complete block;
- no duplicate policy;
- no unrelated content lost.

Stop if either tool rewrites the file outside the managed block.

# Work package 12 — Graph artifacts
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



text
Review Graphify output for Git suitability.

Do not modify .gitignore yet.

Inspect:
- file sizes;
- embedded content;
- absolute paths;
- secrets;
- source commit;
- stability across rebuilds.

Propose which files should be committed and which should remain ignored.

Preferred initial proposal:
- commit graph.json;
- commit GRAPH_REPORT.md;
- ignore graphify-out/cache/;
- ignore graphify-out/cost.json;
- keep graph.html local unless specifically approved.

Show the proposed .gitignore diff and stop.

# Work package 13 — Git hooks
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



Do this only after you have decided that Graphify is genuinely useful.

text
Evaluate Graphify Git hook behaviour.

Do not install the hook yet.

Inspect:
- graphify hook --help;
- current Git hooks;
- current Git configuration;
- whether existing hooks are preserved;
- whether the Graphify hook updates only Graphify output.

Return a risk assessment.

Stop before installation.
After approval:

text
Install the Graphify hook.

Preserve existing hooks.
Do not modify GBrain.
Do not modify AGENTS.md.

Verify:
- graphify hook status;
- existing hooks remain intact;
- the hook updates the intended graph;
- no secrets are written;
- execution time is acceptable;
- the source commit in graph metadata changes after a test commit.

If any condition fails, remove the Graphify hook and report.

# Work package 14 — Optional GBrain skillpack
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
Do not treat a successful command exit code as proof that the task succeeded.

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests

---



Keep this separate:

text
Evaluate GBrain skillpack scaffolding for OpenCode only.

Do not install Hermes or OpenClaw.
Do not modify the live mb-3-cs code repository.
Use makepdlf-project-library as the test workspace.

Inspect the installed skillpack command and workspace syntax first.
Show the command before execution.

After scaffolding, verify:
- SKILL.md files exist;
- RESOLVER.md exists;
- skill frontmatter is present;
- scaffolded skills match the available manifest/resolver;
- no expected skill is silently omitted.

Report the result.
This is not required for Graphify adoption.
---

# Handling DeepSeek V4 Pro safely
DeepSeek V4 Pro is suitable for this task, but configure it as a careful engineering agent, not an autonomous administrator.

Use high reasoning for:

multi-step diagnosis;

command planning;

interpreting graph quality;

reviewing SQL;

resolving contradictory outputs.

Use maximum reasoning only for:

final technical review;

ambiguous cross-system diagnosis;

deciding whether a failure is a real product limitation;

reviewing a potentially destructive migration or hook change.

Do not use maximum reasoning for every shell command. It increases cost and does not improve deterministic operations.

The production V4 Pro release supports tool use and multiple reasoning modes, including high and max effort. Published scores indicate strong agentic coding capability, but benchmark results are vendor or third-party measurements and do not replace your own acceptance tests.

Model-specific guardrails
Add these instructions to the OpenCode task prompt:

text
You are operating a live development environment.

Do not:
- execute destructive SQL without explicit approval;
- modify schema or migrations;
- run gbrain self-upgrade;
- run dream;
- rotate or expose API keys;
- install Git hooks;
- overwrite AGENTS.md;
- remove an existing package installation;
- commit files;
- push to GitHub;
- connect Graphify to GBrain's database;
- continue after a failed verification.

For every action:
1. state the intended change;
2. show the command;
3. execute only within the approved scope;
4. show the result;
5. compare the result with the acceptance criteria;
6. stop if unexpected.
This prevents the model from treating a successful command exit code as proof that the task succeeded.

Where your Anthropic key may still be needed
Your Anthropic key may be required by GBrain’s internal intelligence phases, particularly extract_atoms, depending on your current configuration. Your local reference records that this phase failed when ANTHROPIC_API_KEY was invalid.

Do not give the key to OpenCode unless required for the specific operation. Keep these uses separate:

text
DeepSeek:
OpenCode planning, coding, inspection, and orchestration.

Anthropic:
only GBrain phases or selective independent review that genuinely require it.
If GBrain’s extract_atoms is optional for the Graphify remediation, defer it. You can complete:

source strategy correction;

Graphify graph generation;

cross-file adequacy testing;

MCP integration;

AGENTS.md policy;

graph provenance;

Git/artifact controls;

without making Anthropic a continuous dependency.

If the dream cycle is required later, run only the necessary phase, capture its error output, and set a budget before execution. Do not launch a full dream cycle casually.

Approval gates
You should personally approve these actions:

text
The human developer must personally approve these actions:
GBrain SQL UPDATE statements
GBrain source resynchronization
search-mode change
package removal
PostgreSQL connection configuration
Graphify PostgreSQL access
AGENTS.md modification
Git hook installation
Git artifact tracking
GBrain skillpack scaffolding
any migration or self-upgrade
any commit or push

OpenCode may perform these without additional approval if the results are read-only:
version checks
help output
Git status and commit inspection
source listing
GBrain statistics
Graphify graph queries
graph report inspection
read-only file inspection
read-only MCP tests
Final advice
Use DeepSeek V4 Pro as the primary model. It is adequate for the task when the work is divided into verified packages and when deterministic tools provide the evidence.

Do not use Anthropic as the main operator merely because the task is important. Use it selectively for GBrain phases that explicitly require it or for an independent final review of an ambiguous result.

The correct execution pattern is:

text
DeepSeek plans and operates
Tools produce evidence
You approve state-changing actions
OpenCode stops at every gate
Git/files/tests determine truth
Anthropic is selective escalation
The most important package is the cross-file Graphify adequacy test. If Graphify cannot produce a reproducible, source-verified EXTRACTED path where GBrain currently returns [unresolved], do not proceed with the wider integration.