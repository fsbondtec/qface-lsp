// Bundles the extension client into a single CommonJS file so the published
// VSIX does not have to ship node_modules. `vscode` stays external because it
// is provided by the extension host at runtime.
const esbuild = require("esbuild");

const production = process.argv.includes("--production");
const watch = process.argv.includes("--watch");

/** @type {import('esbuild').BuildOptions} */
const options = {
  entryPoints: ["client/src/extension.ts"],
  bundle: true,
  outfile: "dist/extension.js",
  external: ["vscode"],
  format: "cjs",
  platform: "node",
  target: "node18",
  minify: production,
  sourcemap: !production,
  logLevel: "info",
};

async function main() {
  if (watch) {
    const ctx = await esbuild.context(options);
    await ctx.watch();
  } else {
    await esbuild.build(options);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
