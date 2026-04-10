import { writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");

const RESOURCE_BASE = "https://raw.githubusercontent.com/kwsch/PKHeX/master/PKHeX.Core/Resources/byte";
const OUTPUT_PATH = path.join(rootDir, "assets", "data", "move-legality-pkhex.json");

const FORMAT_CONFIGS = [
  {
    key: "pb7",
    personalFile: "personal_gg",
    personalSize: 0x54,
    levelupFile: "lvlmove_gg.pkl",
    resourceId: "gg",
    formStatsOffset: 0x1c,
    formCountOffset: 0x20,
  },
  {
    key: "pk8",
    personalFile: "personal_swsh",
    personalSize: 0xb0,
    levelupFile: "lvlmove_swsh.pkl",
    resourceId: "ss",
    formStatsOffset: 0x1e,
    formCountOffset: 0x20,
  },
  {
    key: "pa8",
    personalFile: "personal_la",
    personalSize: 0xb0,
    levelupFile: "lvlmove_la.pkl",
    resourceId: "la",
    formStatsOffset: 0x1e,
    formCountOffset: 0x20,
  },
  {
    key: "pk9",
    personalFile: "personal_sv",
    personalSize: 0x50,
    levelupFile: "lvlmove_sv.pkl",
    resourceId: "sv",
    formStatsOffset: 0x18,
    formCountOffset: 0x1a,
  },
  {
    key: "pa9",
    personalFile: "personal_za",
    personalSize: 0x50,
    levelupFile: "lvlmove_za.pkl",
    resourceId: "za",
    formStatsOffset: 0x18,
    formCountOffset: 0x1a,
  },
];

async function main() {
  const output = {};

  for (const format of FORMAT_CONFIGS) {
    output[format.key] = await buildFormatDataset(format);
  }

  await mkdir(path.dirname(OUTPUT_PATH), { recursive: true });
  await writeFile(OUTPUT_PATH, `${JSON.stringify(output)}\n`, "utf8");
  console.log(`Wrote ${OUTPUT_PATH}`);
}

async function buildFormatDataset(format) {
  const [personalBytes, levelupBytes] = await Promise.all([
    fetchBytes(`${RESOURCE_BASE}/personal/${format.personalFile}`),
    fetchBytes(`${RESOURCE_BASE}/levelup/${format.levelupFile}`),
  ]);

  const personalEntries = splitFixedEntries(personalBytes, format.personalSize);
  const levelupEntries = parseBinLinker16(levelupBytes, format.resourceId).map(parseLearnsetEntry);

  const results = {};
  for (let species = 1; species < personalEntries.length; species += 1) {
    const info = readPersonalInfo(personalEntries[species], format);
    const forms = Math.max(info.formCount || 1, 1);

    const baseMoves = collectMovesForEntry({
      formIndex: species,
      levelupEntries,
    });
    addEntry(results, species, 0, baseMoves);

    for (let form = 1; form < forms; form += 1) {
      const formIndex = info.formStatsIndex > 0 ? info.formStatsIndex + form - 1 : species;
      if (formIndex <= 0 || formIndex >= personalEntries.length) continue;
      const formMoves = collectMovesForEntry({
        formIndex,
        levelupEntries,
      });
      if (!areMoveListsEqual(baseMoves, formMoves)) {
        addEntry(results, species, form, formMoves);
      }
    }
  }
  return sortEntries(results);
}

function collectMovesForEntry({ formIndex, levelupEntries }) {
  const moveLevels = new Map();

  const learnset = levelupEntries[formIndex] ?? [];
  for (const [moveId, minLevel] of learnset) {
    mergeMove(moveLevels, moveId, minLevel);
  }

  return Array.from(moveLevels.entries()).sort((a, b) => a[0] - b[0]);
}

function readPersonalInfo(entry, format) {
  return {
    formStatsIndex: readU16(entry, format.formStatsOffset),
    formCount: entry[format.formCountOffset] ?? 1,
  };
}

function addEntry(result, species, form, moves) {
  if (!moves.length) return;
  result[`${species}:${form}`] = moves;
}

function mergeMove(map, moveId, minLevel) {
  if (!moveId) return;
  const prev = map.get(moveId);
  if (prev == null || minLevel < prev) {
    map.set(moveId, minLevel);
  }
}

function sortEntries(result) {
  return Object.fromEntries(
    Object.entries(result).sort(([a], [b]) => {
      const [speciesA, formA] = a.split(":").map(Number);
      const [speciesB, formB] = b.split(":").map(Number);
      return speciesA - speciesB || formA - formB;
    }),
  );
}

function areMoveListsEqual(left, right) {
  if (left.length !== right.length) return false;
  for (let index = 0; index < left.length; index += 1) {
    if (left[index][0] !== right[index][0] || left[index][1] !== right[index][1]) {
      return false;
    }
  }
  return true;
}

function splitFixedEntries(buffer, entrySize) {
  const bytes = asUint8Array(buffer);
  const result = [];
  for (let offset = 0; offset < bytes.length; offset += entrySize) {
    result.push(bytes.slice(offset, offset + entrySize));
  }
  return result;
}

function parseBinLinker16(buffer, expectedIdentifier) {
  const bytes = asUint8Array(buffer);
  const identifier = new TextDecoder("ascii").decode(bytes.subarray(0, 2));
  if (identifier !== expectedIdentifier) {
    throw new Error(`Unexpected BinLinker identifier ${identifier}; expected ${expectedIdentifier}`);
  }
  const count = readU16(bytes, 2);
  const entries = [];
  for (let index = 0; index < count; index += 1) {
    const offset = 4 + index * 2;
    const start = readU16(bytes, offset);
    const end = readU16(bytes, offset + 2);
    entries.push(bytes.slice(start, end));
  }
  return entries;
}

function parseLearnsetEntry(entryBytes) {
  if (!entryBytes?.length) return [];
  const count = Math.floor(entryBytes.length / 3);
  const movesByteLength = count * 2;
  const result = [];
  for (let index = 0; index < count; index += 1) {
    const moveId = readU16(entryBytes, index * 2);
    const level = entryBytes[movesByteLength + index];
    result.push([moveId, level]);
  }
  return result;
}

function parseMoveSourceEntry(entryBytes) {
  if (!entryBytes?.length) return [];
  const result = [];
  for (let offset = 0; offset < entryBytes.length; offset += 2) {
    result.push(readU16(entryBytes, offset));
  }
  return result.filter(Boolean);
}

function readU16(bytes, offset) {
  return bytes[offset] | (bytes[offset + 1] << 8);
}

function asUint8Array(buffer) {
  return buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
}

async function fetchBytes(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch ${url}: ${response.status}`);
  }
  return new Uint8Array(await response.arrayBuffer());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
