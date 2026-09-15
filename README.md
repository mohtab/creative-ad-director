# Creative Ad Director — Hermes skill

Shareable bundle containing the complete creative-ad-director skill and its supporting files. No account credentials, conversation exports or personal project files are included.

## Install

Give this ZIP to your Hermes assistant and say:

> Inspect this ZIP and install the creative-ad-director skill into my active Hermes profile. Preserve its templates, references, scripts and assets folders. If a skill with this name already exists, ask before replacing it. Verify it can be loaded.

The skill folder must retain SKILL.md at its root. Do not install into another profile unintentionally.

## Start creating

> Use creative-ad-director to create an advertisement for [product/service/experience]. Ask only the essential unanswered questions, then deliver a concept, detailed production prompt and separate editing instructions. My video platform is [Higgsfield/Runway/other].

## Contents

- SKILL.md: creative workflow and verification requirements.
- templates/master-prompt.md: production package template.
- references/design-and-model-notes.md: creative lessons and dated platform notes.
- scripts/validate_timeline.py: Python 3 standard-library timeline validator.
- assets/stillwater-timeline.json: fictional example timing manifest; not footage or a complete campaign asset pack.

## Optional checks

From inside the installed creative-ad-director directory:

    python3 scripts/validate_timeline.py --self-test
    python3 scripts/validate_timeline.py assets/stillwater-timeline.json

The validator checks edit-plan arithmetic, not rendered video or spoken performance. Voiceover pacing warnings need a spoken check.

This skill creates concepts and prompts. It does not include video-generation access, credits, licensed music or reference images. Check current official platform documentation before relying on the dated capability notes. Rendering, spending credits and publishing require separate authorization.
