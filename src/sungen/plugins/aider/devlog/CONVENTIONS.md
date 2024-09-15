Purpose: Standardize coding practices with aider to ensure consistency, quality, and adversarial collaboration.
Guiding Principles:
Epistemic Agency Preservation: Always prioritize human decision-making; aider provides alternatives, not directives.
Zero Trust Framework: Do not fully trust AI-generated outputs; always validate and challenge.
Adversarial Collaboration: Encourage aider to offer counter-arguments, alternative implementations.
Coding Guidelines:
Type Safety: Use TypeScript types extensively; ensure strong type checks.
Error Handling: Implement robust error handling; prioritize security, prevent injection attacks.
Logging and Debugging: Add detailed logging to trace AI decisions; maintain transparency in AI recommendations.
Testing Requirements:
Auto-Testing Enabled: Continuous testing with every change; validate all aider-generated code.
Security and Performance Tests: Include edge case and adversarial tests; identify vulnerabilities, performance bottlenecks.
File Management:
Read-Only Files: Protect key files (README.md, CONVENTIONS.md); prevent unintended changes.
Document Changes: All modifications must be documented; update README.md with rationale for changes.
Process Guidelines:
Prompt Pattern: Use explicit prompts for clarity (action: file: details).
Feedback Loop: Actively seek aider feedback; incorporate test results, alternate views.
Selective Committing: Commit after review; avoid auto-commits.
Ethical Considerations:
Transparency: Disclose AI decision-making process; ensure visibility of assumptions and data sources.
Bias Mitigation: Regularly audit for biases in AI outputs; challenge and correct as needed.
Adoption Strategy:
Continuous Improvement: Iteratively refine conventions based on team feedback and AI performance.
Collaborative Documentation: Maintain comprehensive documentation to align all team members on coding standards.