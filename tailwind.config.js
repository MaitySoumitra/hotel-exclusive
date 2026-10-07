/* Tailwind config: edit colours/fonts here, then run `npm run build:css` */
module.exports = {
  content: ["./*.html", "./js/*.js"],
  theme: {
    extend: {
      colors: {
        ink: "#12302f",      // deep lagoon – headings, footer, primary buttons
        brass: "#b98a3e",    // accent – prices, highlights
        mist: "#f4f7f6",     // soft section background
      },
      fontFamily: {
        display: ["Fraunces", "Georgia", "serif"],
        sans: ["'DM Sans'", "system-ui", "sans-serif"],
      },
    },
  },
};
