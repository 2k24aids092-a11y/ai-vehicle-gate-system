module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0f172a',
        secondary: '#1e293b',
        accent: '#06b6d4',
        success: '#10b981',
        danger: '#ef4444',
        warning: '#f59e0b',
      },
      backdropBlur: {
        'xl': '20px',
      },
    },
  },
  plugins: [],
}
