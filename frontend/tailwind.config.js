// frontend/tailwind.config.js
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  safelist: [
    'bg-settings',
  ],
  theme: {
    extend: {
      main: '#F9F8F6',
      settings: '#2C3E50',      
    },
  },
  plugins: [],
};
