<p align="center">
  <img src="./skeleten-logo.png" width="300" alt="SKELETEN Logo">
</p>

# 🩻 SKELETEN  
*The AI-First Technical Documentation & Intent Drift Sentry Engine.*

[![NPM Version](https://img.shields.io/npm/v/skeleten)](https://npmjs.com/package/skeleten)
[![CI Build](https://github.com/eybersjp/Skeleten/actions/workflows/ci.yml/badge.svg)](https://github.com/eybersjp/Skeleten/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**SKELETEN** is an autonomous documentation framework designed to be deployed directly inside your source repository. It parses abstract syntax architectures using `tree-sitter`, cross-references the intelligence with vector similarity via `sentence-transformers`, and actively monitors your intent-to-code gap to identify **Documentation Drift** before bad code ships.

Crucially, **SKELETEN was built for AI Agents**. It automatically injects custom skills and slash commands (`/skeleten-run`) directly into your localized `.agents` configuration, ensuring that LLMs working in your repository *exactly know how to parse context and repair drift safely.*

---

## ⚡ Quick Start

SKELETEN is distributed globally via NPM and installs flawlessly using a single drop-in command:

```bash
npx skeleten init
```

Running this inside the root of your project immediately translates the python core engine into your repository and configures your virtual environment.

## 🏗️ The 4 Phases of SKELETEN

1. **`PHASE_01_CORE`**: Deep AST extraction using recursive Tree-Sitter parsers. Extracts structural elements (Functions, Classes, Context). Assembles initial JSON matrices.
2. **`PHASE_02_VECTOR`**: Sentence Transformer vectorization calculates Cosine Similarities between the raw function names and document tokens. Highlights mismatches.
3. **`PHASE_03_GEN`**: Synthesizes formal `SKELETEN_API_REFERENCE.md` formatted strictly for native Agent consumption with Fenced blocks. 
4. **`PHASE_04_DRIFT`**: Generates pre-commit hooks that strictly analyze the repository. If Code-to-Intent disparity >15%, commits fail automatically safely guarding production.

## 🧠 AI Agent Capabilities

Immediately upon running initialization, SKELETEN provisions your `.agents` configuration path to expose custom workflow hooks. Any compliant contextual AI reading your root can trigger:
- `/skeleten-run` — Runs the extraction architecture across all 4 phases autonomously.
- `/skeleten-health` — Tests SKELETEN schema integrity metrics to guarantee zero false positives.

*You don't just use SKELETEN. Your AI uses SKELETEN.*

## 🔒 Isolated Execution (`venv`)

We recognize that Python dependency scopes (`requirements.txt`) can shatter fragile external mono-repos.
We built SKELETEN's extraction engine to autonomously invoke a `node` child process during execution that guarantees full virtual environment (`venv`) isolation. `run.py` dynamically sniffs `exec_path` strings to force reroutes into `.skeleten/venv`—acting independently of your root interpreter context.

## 🎨 Terminal Branding

To have the SKELETON identity appear every time you open your terminal, appearing alongside the `skeleten` command, add the following block to the end of your `~/.bashrc` or `~/.zshrc` file:

```bash
# KELETEN Terminal Logo - SSTECH Protocol
function keleten_logo() {
    local ORANGE='\033[38;5;208m'
    local WHITE='\033[97m'
    local RESET='\033[0m'

    cat << EOF

${ORANGE}      _________________
     /                /
    /      __________/
   /      /
  /      /____________${WHITE}      _  _________  _      _________  _________  _      _
${ORANGE} /                  /${WHITE}     | |/ /|  ____|| |    |  ____||__   __||  ____|| \    | |
${ORANGE}/___________      _/${WHITE}      | ' / | |__   | |    | |__      | |   | |__   |  \   | |
${ORANGE}           /     /${WHITE}        |  <  |  __|  | |    |  __|     | |   |  __|  | |\ \  | |
${ORANGE} _________/     /${WHITE}         | . \ | |____ | |____| |____    | |   | |____ | | \ \ | |
${ORANGE}/______________/ ${WHITE}         |_|\_\|______||______||______|   |_|   |______||_|  \___|

${ORANGE}  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _   [✓]
${RESET}
EOF
}

# Execute on login
keleten_logo

# Register alias
alias keleten='keleten_logo'
```

## 📜 License
Available underneath standard MIT provisions. Developed cleanly by eybersjp.
