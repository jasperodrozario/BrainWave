/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html", "./base/templates/base/*.html"],
  theme: {
    extend: {
      colors: {
        "subtle-purple": "#5F5E73",
        "subtle-white": "#D8DAE8",
        "light-lavender": "#6A6A95",
        "theme-primary": "#2C2D38",
        "theme-secondary": "#3F4054",
      },
      fontFamily: {
        sans: ['DM Sans', 'sans-serif'],
      }
    },
  },
  plugins: [
    require("tailwind-scrollbar"),
    //Add other plugins
  ],
};
