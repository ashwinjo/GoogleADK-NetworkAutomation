/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-bg': '#000000',
        'dark-panel': '#1a1a1a',
        'accent-red': '#dc2626',
      },
    },
  },
  plugins: [],
}

