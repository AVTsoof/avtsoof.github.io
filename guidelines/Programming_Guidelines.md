
# Programming Guidelines

## Git Guidelines

- **Methodology:**
    
    - Adhere to `Trunk Based Development`. Branches should be short-lived and merge back to the trunk frequently.
        
    - **The Golden Rule:** Treat local history as a "Save Point" (messy allowed) but shared history as a "Story" (must be curated).
        
- **Atomic Commits:**
    
    - **One Logic, One Commit:** A commit must represent a single, complete logical change (e.g., "Add feature X," not "Add feature X and fix typo in Y").
        
    - **Concept over Component:** Never split a logical change across commits (e.g., header in Commit A, source in Commit B). Commit the entire vertical slice required for the "Idea" to work.
        
    - **Revert/Bisect Safe:** Every commit must be reversible in isolation without breaking the rest of the application.
        
- **Build Integrity (The Green Policy):**
    
    - **Bisect-ability:** Every single commit in the shared history _must_ compile and pass tests.
        
    - **Stash-Test-Verify:** When splitting work into atomic commits, ensure `unstaged` changes are not required for the build to pass (use `git stash --keep-index` to verify).
        
    - **The "Vendor Import" Exception:** Non-compilable code is permitted _only_ when establishing a baseline for external code, provided it is excluded from the build system until the subsequent "Integration" commit.
        
- **Commit Messages:**
    
    - **Format:** Separate Subject (50 chars) and Body (72 chars) with a blank line.
        
    - **Mood:** Use Imperative Mood ("Fix bug," not "Fixed bug").
        
    - **Content:** The Body must explain the _Why_ (Context/Architecture), not the _What_ (Diff).
        
- **Workflow & Hygiene:**
    
    - **WIP Strategy:** Prefix incomplete work with `WIP:` or use `wip/` branches. These must never merge to master.
        
    - **Fixup Protocol:** Do not create "Fix typo" commits on top of a feature. Use `git commit --fixup <hash>` to target the original error.
        
    - **Cleanup:** Use `git rebase -i --autosquash` to consolidate WIPs and Fixups into clean atomic units before pushing.
        

## gitignore Guidelines

- **Methodology (The Baseline):**
    
    - **Don't Reinvent the Wheel:** Always initialize with an industry-standard template (e.g., [gitignore.io](https://www.toptal.com/developers/gitignore)).
        
    - **Composite Templates:** If using multiple technologies (e.g., C++ backend + Python scripts), concatenate the standard templates for both.
        
- **Scope & Hierarchy:**
    
    - **Artifacts over Source:** Ignore _anything_ generated from source. If it can be recreated by a build command, it does not belong in the repo (e.g., `bin/`, `obj/`, `dist/`, `node_modules/`).
        
    - **Pragmatic Pollution Control:** Add OS files (`.DS_Store`) and IDE folders (`.vs/`, `.idea/`) to the project `.gitignore`, even if they belong in a global config, to prevent accidental pollution by teammates.
        
- **Security & Configuration:**
    
    - **Secrets Zero Tolerance:** Explicitly ignore local config files holding secrets (e.g., `.env`).
        
    - **The Template Pattern:** If ignoring a config file (e.g., `config.local.json`), you _must_ commit a sanitized template (e.g., `config.example.json`).
        
- **Syntax & Maintenance:**
    
    - **Whitelisting Strategy:** To track a specific file type that is generally ignored, use the `!` operator _after_ the ignore rule (e.g., `!vendor/lib/special.dll`).
        
    - **The "Cached" Trap:** If a file was already committed, adding it to `.gitignore` does nothing. Run `git rm --cached <file>` to stop tracking it while keeping it on disk.
        

## General Programming Principles (Language Agnostic)

- **Clean Code & Naming:**
    
    - **Self-Documenting Code:** Variable and function names should be descriptive enough that comments are unnecessary.
        
    - **Comment the "Why":** Comments should explain _intent_ or _business logic_ reasons, never the _syntax_ or _what_ the code is doing.
        
    - **Magic Literals:** Replace raw strings and numbers inside logic with **Named Constants** or **Enums** (e.g., `MAX_RETRY_COUNT` instead of `3`).
        
- **Function Architecture:**
    
    - **Single Responsibility Principle (SRP):** A function should do one thing and do it well. If a function contains the word "And" in its description, it likely needs splitting.
        
    - **Guard Clauses:** Prefer returning early (e.g., `if (error) return;`) over deeply nested `if/else` blocks to improve readability.
        
    - **Pure Functions:** Where possible, avoid side effects. Output should strictly depend on Input.
        
- **Robustness & Safety:**
    
    - **Fail Fast:** Validate inputs at the very beginning of a function/script. Crash early rather than processing corrupted data.
        
    - **Logging over Printing:** Never use standard output (print/cout) for application logs. Use a dedicated logging framework with levels (DEBUG, INFO, ERROR).
        
    - **Deterministic Output:** When processing data sets, always sort inputs/outputs (e.g., by ID or timestamp) to ensure consistent checksums and easier diffing.
        
- **Interface Flexibility:**
    
    - **Hybrid Execution:** Scripts/Tools should support both specific targets (Single File Mode) and auto-scanning (Batch Mode) depending on arguments provided.
        

## Python Specific Guidelines

- **Environment & Dependencies:**
    
    - **Standard Library First:** Prioritize built-in packages (e.g., `os`, `sys`, `json`) over third-party dependencies.
        
    - **Path Handling:** Always use `from pathlib import Path` over string manipulation for file paths.
        
- **Interface:**
    
    - **Argument Parsing:** Use `argparse` for robustness and auto-generated help menus.
        
- **Type Safety:**
    
    - **Type Hinting:** Use the `typing` module (e.g., `List`, `Optional`) for all function signatures to enforce contract clarity.
        
