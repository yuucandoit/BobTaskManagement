/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ibm: {
          blue: "#0f62fe",
          darkblue: "#0043ce",
          gray: "#161616",
          lightgray: "#f4f4f4",
          cardbg: "#1e1e1e",
        }
      }
    },
  },
  plugins: [],
}
