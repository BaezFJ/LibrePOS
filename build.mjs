import { readdirSync } from "node:fs";
import { join } from "node:path";
import * as esbuild from "esbuild";

const STATIC = "src/librepos/app/static";
const CSS_DIR = join(STATIC, "css");
const JS_DIR = join(STATIC, "js");

const args = process.argv.slice(2);
const watch = args.includes("--watch");
const filter = args.find((a) => a !== "--watch"); // "css", "js", or undefined

function sourceFiles(dir, ext) {
  return readdirSync(dir)
    .filter((f) => f.endsWith(ext) && !f.endsWith(`.min${ext}`))
    .map((f) => join(dir, f));
}

async function minify(files, loader) {
  for (const file of files) {
    const ext = loader === "css" ? ".css" : ".js";
    const out = file.replace(ext, `.min${ext}`);

    if (watch) {
      const ctx = await esbuild.context({
        entryPoints: [file],
        outfile: out,
        minify: true,
        bundle: false,
        logLevel: "info",
      });
      await ctx.watch();
    } else {
      await esbuild.build({
        entryPoints: [file],
        outfile: out,
        minify: true,
        bundle: false,
        logLevel: "info",
      });
    }
  }
}

if (!filter || filter === "css") {
  await minify(sourceFiles(CSS_DIR, ".css"), "css");
}

if (!filter || filter === "js") {
  await minify(sourceFiles(JS_DIR, ".js"), "js");
}

if (watch) {
  console.log("\nWatching for changes...");
}
