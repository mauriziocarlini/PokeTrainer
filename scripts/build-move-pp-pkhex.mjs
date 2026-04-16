import { writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");

const SOURCE_BASE = "https://raw.githubusercontent.com/kwsch/PKHeX/master/PKHeX.Core/Moves";
const OUTPUT_PATH = path.join(rootDir, "assets", "data", "move-pp-pkhex.json");

const FORMAT_SOURCES = {
  pb7: "MoveInfo7b.cs",
  pk8: "MoveInfo8.cs",
  pb8: "MoveInfo8.cs",
  pa8: "MoveInfo8a.cs",
  pk9: "MoveInfo9.cs",
  pa9: "MoveInfo9a.cs",
};

async function main() {
  const output = {};
  for (const [formatKey, sourceFile] of Object.entries(FORMAT_SOURCES)) {
    const source = await fetchText(`${SOURCE_BASE}/${sourceFile}`);
    output[formatKey] = extractPpTable(source, sourceFile);
  }

  await mkdir(path.dirname(OUTPUT_PATH), { recursive: true });
  await writeFile(OUTPUT_PATH, `${JSON.stringify(output)}\n`, "utf8");
  console.log(`Wrote ${OUTPUT_PATH}`);
}

function extractPpTable(source, sourceFile) {
  const match = source.match(/public static ReadOnlySpan<byte> PP =>\s*\[([\s\S]*?)\];/);
  if (!match) throw new Error(`Could not find PP table in ${sourceFile}`);
  return match[1]
    .replace(/\/\/.*$/gm, "")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean)
    .map((value) => Number.parseInt(value, 10));
}

async function fetchText(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Failed to fetch ${url}: ${response.status}`);
  return response.text();
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
