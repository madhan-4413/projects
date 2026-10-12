---
name: generate-changelog-pdf
description: >-
  Generates a clean, beautifully formatted PDF changelog (changeslog.pdf) documenting project session changes, file modifications, rationales, and technical summaries using ReportLab. Use this skill whenever the user requests a PDF changelog, session summary PDF, or changeslog.pdf generation.
---

# Generate Changelog PDF Skill

This skill provides a Python script and automated procedure to compile session changes, architectural updates, secret management additions, and file modifications into a professional PDF changelog (`changeslog.pdf`) using ReportLab.

## When to Use

Use this skill when:
- The user requests a PDF summary or changelog of session updates.
- Creating `changeslog.pdf` or similar project progress reports.
- Documenting multi-file refactoring with detailed bullet points and "Why" rationales.

## Instructions

1. **Gather Session Data**:
   Collect all file changes (modified, created, deleted), feature updates, security changes, and their respective rationales.

2. **Execute Changelog Generator Script**:
   Run the changelog script using Python:
   ```bash
   python .agents/skills/generate-changelog-pdf/scripts/generate_changelog.py
   ```

3. **Verify Output**:
   Confirm that `changeslog.pdf` was generated successfully in the root directory.

## Script & Resources

- Script: [generate_changelog.py](./scripts/generate_changelog.py)
