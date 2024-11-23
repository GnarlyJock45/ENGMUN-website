/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
    // Add any other files that contain Tailwind classes
  ],
  theme: {
    extend: {
      // Your customizations
      colors: {
        primary: '#4F7B7B',
        secondary: '#C6943B',
      },
    },
  },
  plugins: [],
}