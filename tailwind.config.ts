import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#111827",
        cloud: "#F6F7FB",
        mint: "#15B88F",
        coral: "#FF6B5F",
        cobalt: "#3157E7",
        graphite: "#242936"
      },
      boxShadow: {
        soft: "0 20px 70px rgba(17, 24, 39, 0.11)"
      }
    }
  },
  plugins: []
};

export default config;
