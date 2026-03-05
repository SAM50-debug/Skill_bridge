/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './apps/**/*.py',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        neon: {
          purple: '#b026ff',
          cyan: '#00f0ff',
        },
        dark: '#0F0F1A',
        card: '#1A1A2E',
      }
    }
  },
  plugins: [],
}
