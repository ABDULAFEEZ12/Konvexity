module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        'primary-deep': '#0A0E27',
        'primary': '#0F1535',
        'accent-gold': '#C8A96E',
        'accent-gold-alt': '#D4AF37',
        'neutral': {
          200: '#E8ECF2',
          300: '#D1D6E0',
          400: '#8B92A5',
          500: '#6B7280',
          600: '#4B5563',
        },
      },
      fontFamily: {
        'sans': ['Inter', '-apple-system', 'sans-serif'],
        'display': ['Playfair Display', 'Georgia', 'serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.8s cubic-bezier(0.25, 0.1, 0.25, 1.0) forwards',
        'bounce': 'bounce 2s infinite',
      },
    },
  },
  plugins: [],
};