# Creative Ad Director

An open, MIT-licensed workflow for turning a product, service or experience into an original cinematic advertising concept and production prompt. Created by Mohtab Arabiat with AI assistance.

**Ask the right questions → establish the promise and proof → design shots → lock continuity → separate generation and editing → verify the plan.**

## Choose your platform

### Hermes
[Download the skill ZIP](https://github.com/mohtab/creative-ad-director/raw/main/creative-ad-director.zip). Give it to your assistant: “Inspect and install this skill into my active Hermes profile. Ask before replacing an existing version. Verify you can load creative-ad-director.” Preserve the complete folder structure.

### Claude
Use the same [skill ZIP](https://github.com/mohtab/creative-ad-director/raw/main/creative-ad-director.zip). Where Skills are enabled, enable code execution/file creation, then open Customize → Skills → + Create skill → Upload a skill. Upload the ZIP and enable it. Workspace policies can restrict this. If unavailable, use the plain-text edition below.

### ChatGPT
1. Create a ChatGPT Project.
2. Add [CREATIVE-AD-DIRECTOR.txt](editions/CREATIVE-AD-DIRECTOR.txt) as a reference file (or paste its contents as a source).
3. Copy [PROJECT-INSTRUCTIONS.txt](editions/PROJECT-INSTRUCTIONS.txt) into the project's instructions.
4. Start with [STARTER-PROMPT.txt](editions/STARTER-PROMPT.txt).
5. For automated timing checks, also provide scripts/validate_timeline.py and your timing JSON to a Python-capable session, or run them locally. The plain-text edition does not include executable Python.

This is a Project/reference workflow, not a claim that ChatGPT installs native skill ZIPs.

### Any other assistant
Paste or attach [the self-contained text edition](editions/CREATIVE-AD-DIRECTOR.txt), then the starter prompt. Browsing, file inspection and code execution depend on the host. Without a tool, the assistant must disclose that the corresponding check was not run.

## What you get
A brief, recommended creative route, campaign hook/proof/payoff/CTA, shot sequence, continuity rules, generation settings with uncertainty disclosed, and separate voiceover/music/branding/editing instructions. The skill does not generate footage itself or supply credits, music rights or reference images.

## Source and downloads
- [SKILL.md](SKILL.md): canonical workflow.
- [Master template](templates/master-prompt.md).
- [Production notes](references/design-and-model-notes.md).
- [Original fictional example](examples/desk-organizer.md).
- [All-platform bundle](https://github.com/mohtab/creative-ad-director/raw/main/creative-ad-director-all-platforms.zip).
- [License](LICENSE) and [rights boundaries](NOTICE.md).

From the repository root:

```sh
python3 scripts/validate_timeline.py --self-test
python3 scripts/validate_timeline.py assets/example-timeline.json
python3 tools/package.py
```

No Python dependencies are required. Timing checks validate an edit plan, not generated footage, voice performance or advertising effectiveness. Platform/model limits must be rechecked; identical output across assistants is not promised.

## Verification scope
Packaging, self-contained text generation, archive integrity and validator tests are checked locally. Installation guidance follows official documentation; this release has not been account-tested inside ChatGPT or Claude. Test your first prompt after installation.

## Contribute
Open an issue or pull request for clearer instructions, examples or validator fixes. Do not submit credentials, client confidential material or assets you lack permission to share. Keep the workflow platform-neutral; do not add unsupported platform promises. Retain the license notice when redistributing.

Official setup references: [Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) · [ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt).
