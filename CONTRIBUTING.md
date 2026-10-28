# Contributing to LinkScope Docs

Thank you for improving this portfolio project. The goal is to make every update technically credible, task-focused, and easy to review.

## Documentation change workflow

1. Open an issue that identifies the reader, task, and evidence for the proposed change.
2. Draft the update in the closest content type: guide, reference, troubleshooting, or style guide.
3. Ask one subject-matter reviewer and one documentation reviewer to check the pull request.
4. Run the test suite and regenerate reports if the reporting logic or sample telemetry changes.
5. Check links, headings, units, terminology, and that examples contain no sensitive data.
6. Merge only after reviewer feedback is resolved in the document or tracked as follow-up work.

## Definition of done

- The reader and their goal are stated or evident.
- Terms match `docs/style-guide.md`.
- Numeric limits include units and scope.
- Procedures include a success signal or expected outcome.
- Screenshots, logs, and sample data are sanitized.
- Generated artifacts are refreshed when their input or generator changes.

## Review checklist

| Reviewer | Checks |
| --- | --- |
| Subject-matter expert | Technical accuracy, limits, safe handling, correct escalation evidence. |
| Technical writer | Task flow, information architecture, terminology, scanability, accessibility. |
| Maintainer | Tests, generated outputs, versioning, release readiness. |
