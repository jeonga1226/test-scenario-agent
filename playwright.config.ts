import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  timeout: 15_000,
  expect: { timeout: 3_000 },
  workers: 4,
  reporter: [["json", { outputFile: "test-results/results.json" }], ["line"]],
  use: {
    baseURL: process.env.BASE_URL ?? "http://localhost:5173",
    headless: true,
    actionTimeout: 5_000,
    screenshot: "only-on-failure",
  },
});
