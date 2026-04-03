#!/usr/bin/env node
/**
 * KB Auto-Compile Check Hook
 *
 * PostToolUse hook that detects when a file is written to a KB vault's raw/ directory
 * and nudges the user to run /kb-compile.
 *
 * Trigger: PostToolUse on Write tool
 */

const fs = require('fs');
const path = require('path');

function main() {
  let input;
  try {
    input = JSON.parse(fs.readFileSync(0, 'utf8'));
  } catch {
    process.exit(0);
  }

  const toolName = input.tool_name || '';
  if (toolName !== 'Write' && toolName !== 'write_file') {
    process.exit(0);
  }

  // Get the file path from tool input
  const filePath = input.tool_input?.file_path || input.tool_input?.path || '';
  if (!filePath) {
    process.exit(0);
  }

  // Normalize path separators
  const normalized = filePath.replace(/\\/g, '/');

  // Check if the file is in a raw/ directory
  const rawMatch = normalized.match(/^(.+?)\/raw\//);
  if (!rawMatch) {
    process.exit(0);
  }

  const vaultRoot = rawMatch[1];

  // Verify this is actually a KB vault (has _meta/ directory)
  const metaDir = path.join(vaultRoot.replace(/\//g, path.sep), '_meta');
  if (!fs.existsSync(metaDir)) {
    process.exit(0);
  }

  // Output nudge in Claude Code hook protocol format
  const fileName = path.basename(filePath);
  const result = {
    decision: "approve",
    reason: `New source "${fileName}" added to KB vault. Run /kb-compile to process it into the wiki.`
  };
  console.log(JSON.stringify(result));
  process.exit(0);
}

main();
