const responseNode = document.querySelector("#codex-response");
const taskListNode = document.querySelector("#task-list");
const copyButton = document.querySelector(".copy-message");
const messageActions = document.querySelector(".message-actions");
const copyStatus = document.querySelector(".copy-status");
const helpTrigger = document.querySelector(".help-trigger");
const helpModal = document.querySelector(".help-modal");
const userStep = document.querySelector('[data-chat-step="user"]');
const agentStep = document.querySelector('[data-chat-step="agent"]');
let copyStatusTimer = null;

const adoptionPrompt = `Use this kit to apply harness engineering to this repository:

https://github.com/baskduf/harness-starter-kit

Clone the kit into ./harness-starter-kit if it is not already present, read it,
then apply its prompt-first harness engineering workflow to this repository.

Requirements:
- Treat the current working directory as the target repository.
- Treat ./harness-starter-kit as read-only reference material after cloning.
- Inspect this repository before editing.
- Preserve existing architecture, tools, package manager, commands, docs, and
  conventions.
- Do not blindly copy templates.
- Add only the minimum useful harness pieces.
- Prefer updating existing docs/configs over duplicating them.
- Do not overwrite or delete existing files without explaining why.
- If I ask for /harness doctor, use
  ./harness-starter-kit/commands/harness-doctor.md.
- If I ask for /harness update after adoption, use
  ./harness-starter-kit/commands/harness-update.md to refresh the kit reference,
  record .harness/source.json, and selectively update target harness files
  without blindly overwriting existing files.

Expected result:
- project-specific AGENTS.md or updated existing agent instructions
- knowledge store if no equivalent exists
- lightweight drift checks based on this repo's real rules
- local verification commands using existing tools
- adoption report with files changed, checks to run, assumptions, remaining
  manual steps, and whether ./harness-starter-kit should be removed, ignored, or
  kept before commit`;

const responses = [
  "Parsed the pasted markdown prompt.",
  "Reading repo rules and constraints.",
  "Planning minimal harness edits.",
  "Preparing the adoption report.",
];

const taskSets = [
  [
    ["Inspect", "done", "done"],
    ["Rules", "active", "running"],
    ["Checks", "pending", "queued"],
    ["Report", "pending", "queued"],
  ],
  [
    ["Inspect", "done", "done"],
    ["Rules", "done", "done"],
    ["Checks", "active", "running"],
    ["Report", "pending", "queued"],
  ],
  [
    ["Inspect", "done", "done"],
    ["Rules", "done", "done"],
    ["Checks", "done", "done"],
    ["Report", "active", "running"],
  ],
];

let responseIndex = 0;
let taskIndex = 0;
let timer = null;

function typeText(text) {
  clearInterval(timer);
  responseNode.textContent = "";

  let cursor = 0;
  timer = setInterval(() => {
    responseNode.textContent = text.slice(0, cursor + 1);
    cursor += 1;

    if (cursor >= text.length) {
      clearInterval(timer);
    }
  }, 22);
}

function renderTasks(tasks) {
  taskListNode.innerHTML = "";

  tasks.forEach(([label, state, status]) => {
    const item = document.createElement("li");
    item.className = `is-${state}`;

    const text = document.createElement("span");
    text.textContent = label;

    const stateLabel = document.createElement("span");
    stateLabel.className = "run-state";
    stateLabel.textContent = status;

    item.append(text, stateLabel);
    taskListNode.append(item);
  });
}

function advance() {
  responseIndex = (responseIndex + 1) % responses.length;
  taskIndex = (taskIndex + 1) % taskSets.length;
  typeText(responses[responseIndex]);
  renderTasks(taskSets[taskIndex]);
}

renderTasks(taskSets[0]);
responseNode.textContent = "";

setTimeout(() => {
  userStep?.classList.add("is-visible");
}, 350);

setTimeout(() => {
  agentStep?.classList.add("is-visible");
  typeText(responses[0]);
}, 1150);

setTimeout(() => {
  setInterval(advance, 4200);
}, 3600);

copyButton?.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(adoptionPrompt);
    copyButton.setAttribute("aria-label", "Copied prompt");
    if (copyStatus && messageActions) {
      copyStatus.textContent = "Copied";
      messageActions.classList.add("is-copied");
      clearTimeout(copyStatusTimer);
      copyStatusTimer = setTimeout(() => {
        messageActions.classList.remove("is-copied");
        copyButton.setAttribute("aria-label", "Copy prompt");
      }, 1400);
    }
  } catch {
    copyButton.setAttribute("aria-label", "Copy unavailable");
    if (copyStatus && messageActions) {
      copyStatus.textContent = "Unavailable";
      messageActions.classList.add("is-copied");
      clearTimeout(copyStatusTimer);
      copyStatusTimer = setTimeout(() => {
        messageActions.classList.remove("is-copied");
        copyButton.setAttribute("aria-label", "Copy prompt");
      }, 1400);
    }
  }
});

function setHelpOpen(isOpen) {
  if (!helpModal) {
    return;
  }

  helpModal.classList.toggle("is-open", isOpen);
  helpModal.setAttribute("aria-hidden", String(!isOpen));
}

helpTrigger?.addEventListener("click", () => {
  setHelpOpen(true);
});

document.querySelectorAll("[data-help-close]").forEach((node) => {
  node.addEventListener("click", () => {
    setHelpOpen(false);
  });
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    setHelpOpen(false);
  }
});
