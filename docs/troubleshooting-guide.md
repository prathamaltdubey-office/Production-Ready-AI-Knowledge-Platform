# Troubleshooting Guide — Production-Ready AI Knowledge Platform

Real issues encountered while building and deploying this project, and how they were resolved.

---

## 1. `docker` command not recognized

**Symptom**

```
docker : The term 'docker' is not recognized as the name of a cmdlet...
```

**Cause** Docker Desktop isn't installed, or the project is actually set up for **Podman** (note the `Containerfile` naming instead of `Dockerfile`).

**Fix** Check which container engine is available:

```powershell
podman --version
```

If Podman is installed, use `podman compose` instead of `docker compose` throughout this project.

---

## 2. Podman: "Cannot connect to Podman... target machine actively refused it"

**Symptom**

```
Cannot connect to Podman. Please verify your connection to the Linux system...
Error: unable to connect to Podman socket: failed to connect: dial tcp 127.0.0.1:PORT
```

**Cause** Podman on Windows runs containers inside a Linux VM (via WSL2). This error means the VM (`podman machine`) isn't running.

**Fix**

```powershell
podman machine list
podman machine start
```

If no machine exists yet:

```powershell
podman machine init
podman machine start
```

---

## 3. Podman machine start fails: "Logon failure: the user has not been granted the requested logon type"

**Symptom**

```
Logon failure: the user has not been granted the requested logon type at this computer.
Error code: Wsl/Service/CreateInstance/CreateVm/HCS/0x80070569
```

**Cause** A Windows local security policy is blocking the "Log on as a batch job" right needed to start a WSL2-backed VM. This is common on **corporate/managed laptops** where IT policy restricts this.

**Fix options**

1. Restart WSL and retry:

   ```powershell
   wsl --shutdown
   podman machine start
   ```
2. Try running the terminal as Administrator.
3. Check WSL health:

   ```powershell
   wsl --status
   wsl --list --verbose
   ```
4. If the machine is IT-managed, this may require IT to grant the necessary local security policy rights — it is not always fixable from a standard user account.

**Workaround if local containers can't run** Local container testing isn't strictly required to prove the deployment config is correct. GitHub Actions' `docker-build` CI job builds both containers on GitHub's own Linux runners, independent of any local WSL/Podman restrictions — use that as the source of truth for "does this build?" when local testing is blocked.

---

## 4. PowerShell `curl` shows a "Script Execution Risk" prompt

**Symptom**

```
Security Warning: Script Execution Risk
Invoke-WebRequest parses the content of the web page...
```

**Cause** PowerShell's built-in `curl` alias maps to `Invoke-WebRequest`, which by default warns before parsing HTML/script content.

**Fix** For simple API checks, skip the prompt:

```powershell
curl -UseBasicParsing http://localhost:8000/api/v1/health
```

---

## 5. Secrets hardcoded in `compose.yaml`

**Symptom** Tokens and URLs written directly under `environment:` in `compose.yaml`, e.g. `API_TOKEN: customer-churn-secret-token`, risking accidental commits of secrets.

**Fix** Use `env_file:` to load values from `.env` / `frontend/.env` instead of hardcoding them, and reference `${VAR}` syntax for Compose `build.args`:

```yaml
services:
  backend:
    env_file:
      - .env
  frontend:
    build:
      args:
        VITE_API_BASE_URL: ${VITE_API_BASE_URL}
    env_file:
      - frontend/.env
```

Confirm `.env` files are listed in `.gitignore`, and commit `.env.example` files with placeholder values instead.

---

## 6. CI `lint` job fails on Black even though it passes locally

**Symptom**

```
would reformat .../app/app.py
Error: Process completed with exit code 1.
```

...despite `black --check .` passing locally.

**Cause** Version drift: the locally installed Black version differs from the version CI installs (`pip install black` grabs the latest release, which may format code differently from an older pinned version — especially around multi-line string formatting).

**Fix** Pin the exact Black version in both places so local and CI environments always agree, matching whatever version `.pre-commit-config.yaml` uses:

```yaml
# ci.yml
- name: Install lint dependencies
  run: pip install ruff==<X> black==<Y> isort==<Z>
```

```powershell
# locally
pip install black==<Y>
```

Then re-run `black .` locally to reformat with the correct version before committing.

---

## 7. Ruff and isort disagree on import order (flip-flopping fixes)

**Symptom** Running `ruff check . --fix` fixes an import order issue, but `isort --check-only .` then reports the same file as incorrectly sorted — and vice versa, indefinitely.

**Cause** Ruff's built-in isort-compatible rule (`I001`) and the standalone `isort` tool can produce slightly different output for certain import patterns (e.g. mixing `from X import a as b` with grouped `from X import (c, d)` imports from the same module), even with `profile = "black"` configured for isort.

**Fix** Pick one tool to own import sorting, not both. Since `.pre-commit-config.yaml` in this project already relies on `isort` (with `ruff --ignore=I` locally), make this consistent everywhere:

```toml
# pyproject.toml
[tool.ruff.lint]
select = ["E", "F"]   # exclude "I" — isort owns import order instead
```

Then ensure `isort --check-only .` is part of the CI `lint` job, matching what pre-commit already enforces.

---

## 8. Pre-commit hook blocks a commit ("files were modified by this hook")

**Symptom**

```
black....................................................................Failed
- hook id: black
- files were modified by this hook
```

The `git commit` command exits without actually creating a commit.

**Cause** This is expected behavior, not an error: pre-commit hooks run Black/isort/Ruff before the commit completes, and if they reformat any files, the commit is intentionally blocked so those changes can be reviewed and included.

**Fix** Re-stage the now-reformatted files and commit again:

```powershell
git add .
git commit -m "your message"
```

The second attempt succeeds once there's nothing left to reformat.

---

## 9. Backend reports `"ollama": "down"` in the health check

**Symptom**

```json
{ "status": "degraded", "ollama": "down", "faiss_index": "loaded" }
```

**Cause** Ollama isn't running on the host, or `OLLAMA_BASE_URL` doesn't match how the container reaches the host.

**Fix**

1. Confirm Ollama is running: `ollama serve` (in a separate terminal)
2. Confirm the URL in `.env`:

   ```env
   OLLAMA_BASE_URL=http://host.containers.internal:11434
   ```

   (`host.containers.internal` is the Podman/Docker convention for "the host machine," from inside a container.)
3. Re-check: `curl -UseBasicParsing http://localhost:8000/api/v1/health`

---

## 10. `401 Unauthorized` on protected endpoints

**Symptom**

```json
{ "detail": "Invalid authentication token" }
```

**Cause** The frontend's `VITE_API_TOKEN` and the backend's `API_TOKEN` don't match, or the `Authorization: Bearer <token>` header isn't being sent.

**Fix** Confirm both `.env` (root) and `frontend/.env` have identical token values, then rebuild the frontend container (Vite env vars are baked in at build time, so a stale build won't pick up a changed token without `--build`):

```powershell
podman compose up --build
```