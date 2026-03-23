# Build Contract: UICare-System

## Current State (Honest)

- Full-stack web app at `uicare-system/`
- Web UI in web/ directory (Next.js / React)
- AI service with GPT-4o-mini integration (aiService.js)
- Docker + docker-compose configuration
- Kubernetes deployment.yaml exists
- Memory-bank architecture (brain module with embeddings)
- Last commit: Mar 17, 2026

## Target State (What Resume Claims)

"Partial | GPT-4o-mini + Kubernetes | Monitors Docker containers for stalled workflows | Web UI, memory-bank architecture"

## Acceptance Criteria

1. `npm install` succeeds in web/
2. `npm run dev` starts the dev server
3. `docker build .` succeeds
4. GPT-4o-mini integration confirmed in source (aiService.js)
5. Kubernetes deployment.yaml exists with valid config
6. Memory-bank / brain module exists in source

## Evidence Required

```bash
cd /Users/coreyalejandro/Projects/uicare-system
npm install
npm run dev &
docker build -t uicare-test .
grep -r "gpt-4o-mini" --include="*.js" --include="*.ts"
cat deployment.yaml | head -20
ls brain/ || ls memory-bank/ || find . -name "*brain*" -o -name "*memory*"
```

## Implementation Spec

No new code needed. Verification only.

## Repo Path

`/Users/coreyalejandro/Projects/uicare-system/`
