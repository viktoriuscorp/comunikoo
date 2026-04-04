/** @type {import('tailwindcss').Config} */
module.exports = {
  content: {
    files: [
      "./**/*.html",
      "./generate_stitch.py",
    ],
    extract: undefined,
    transform: undefined,
  },
  // Exclude node_modules from content scanning
  safelist: [],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary": "#001e40",
        "primary-container": "#003366",
        "on-primary": "#ffffff",
        "on-primary-container": "#c8d6e5",
        "secondary-container": "#fd8b00",
        "on-secondary-container": "#603100",
        "secondary": "#e07a00",
        "surface": "#fdfdfd",
        "surface-container-low": "#f4f6fa",
        "surface-container-lowest": "#ffffff",
        "surface-container-high": "#e8ebf0",
        "on-surface": "#1a1c1e",
        "on-surface-variant": "#43474f",
        "on-background": "#1a1c1e",
        "outline-variant": "#c4c7cf",
        "on-tertiary-container": "#43474f",
      },
      fontFamily: {
        headline: ["Poppins", "sans-serif"],
        body: ["Poppins", "sans-serif"],
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
  ],
}
