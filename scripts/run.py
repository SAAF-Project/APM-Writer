"""Entry point of the APM-Writer: drafts one section of the Audit Planning Memorandum per session.

    python scripts/run.py

Skeleton only: the workflow steps are laid out as comments and placeholders.
"""

# Sections the agent can write. Update this list to add or remove sections.
available_sections = ['2.6.1', '2.6.2', '2.6.3']


def main():
    # -------------------- Overview and section selection --------------------
    # Show which APM sections the agent can write (available_sections), with what each one
    # expects from the user and what it delivers.
    # Show the selection board and ask which section to write (one section per session).
    # Only a value from available_sections is accepted.
    selected_section = None  # placeholder

    # -------------------- Step 1: Audit scoping --------------------
    # Open with "What is your audit about?", then ask one question at a time:
    #   - audit objective
    #   - in scope / out of scope
    #   - audit period
    #   - business lines, entities, product groups (if relevant)
    # If an answer is vague, propose 2-3 structured options instead of an open follow-up.
    # Close with a short summary and let the user confirm or correct it.
    audit_scope = None  # placeholder

    # -------------------- Step 2: Document intake and validation --------------------
    # Ask for the mandatory documents of the selected section, and leave room for extra documents.
    # After upload, do not draft yet. For each document: type, short content summary,
    # and why it is relevant for this audit. Let the user confirm the interpretation.
    # If a mandatory document is missing, ask for it one item at a time.
    documents = None  # placeholder

    # -------------------- Step 3: Deepening understanding --------------------
    # Refine the scope iteratively with targeted questions driven by the documents
    # (period, business unit, coverage), one question at a time.
    # After each refinement give a scope update: in scope / out of scope / unclear, to confirm.
    # Repeat until scope and inputs are clear and confirmed.
    refined_scope = None  # placeholder

    # -------------------- Step 4: Synthesis and writing --------------------
    # Synthesise across all documents (consistency vs contradictions, risk signals, trends).
    # Write the section in its defined structure and apply the writing rules:
    # max 8 paragraphs, 4-6 lines each, ~70% conclusions / 30% evidence,
    # each part concludes what should be in the audit scope. Run the final quality check.
    section_text = None  # placeholder

    # -------------------- Save the section locally --------------------
    # Save only the written section to a local file and tell the user the path.
    output_path = None  # placeholder


if __name__ == "__main__":
    main()
