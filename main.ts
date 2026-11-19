// main.ts — copies POST.json (the X post address) to the output dir.
//
// Run the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
// Prints nothing on success. No network, no wall clock, no files
// outside the repository; the two runs of an entry write the same bytes.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const URL_RE =
  /^https:\/\/(?:x\.com|twitter\.com)\/(?:[A-Za-z0-9_]+|%3Chandle%3E|<handle>)\/status\/(?:\d+|<id>)$/;

function fail(message: string): never {
  console.error(message);
  process.exit(1);
}

const botDir = process.env.MAKEFUN_BOT_DIR;
if (!botDir) fail("MAKEFUN_BOT_DIR is not set");
const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) fail("MAKEFUN_OUTPUT_DIR is not set");

const srcPath = join(botDir, "POST.json");
const raw = readFileSync(srcPath);

let data: unknown;
try {
  data = JSON.parse(raw.toString("utf8"));
} catch {
  fail("POST.json is not valid JSON");
}

if (typeof data !== "object" || data === null || Array.isArray(data)) {
  fail("POST.json must be a JSON object");
}
const url = (data as Record<string, unknown>).url;
if (typeof url !== "string" || !URL_RE.test(url)) {
  fail("POST.json url is not an X post address");
}

mkdirSync(outDir, { recursive: true });
const dstPath = join(outDir, "POST.json");
writeFileSync(dstPath, raw);

// Verify the copy byte-for-byte.
const copied = readFileSync(dstPath);
if (!copied.equals(raw)) {
  fail("POST.json copy differs from the original");
}
