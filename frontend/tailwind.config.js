/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ni: {
          bg: "#0a0a1a",
          surface: "#12122a",
          card: "rgba(255,255,255,0.05)",
          border: "rgba(255,255,255,0.08)",
          accent: "#6366f1",
          "accent-light": "#818cf8",
          cyan: "#22d3ee",
          emerald: "#34d399",
          rose: "#fb7185",
          amber: "#fbbf24",
          text: "#e2e8f0",
          muted: "#94a3b8",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      backdropBlur: {
        glass: "16px",
      },
    },
  },
  plugins: [],
};
