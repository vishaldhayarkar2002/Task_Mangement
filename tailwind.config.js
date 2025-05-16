/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/www/**/*.{html,jinja}',
    './t_app/public/js/**/*.js',
    './t_app/templates/**/*.html',
    '../../erpnext/erpnext/public/js/**/*.js',
    '../../erpnext/erpnext/templates/**/*.html',
    './t_app/public/**/*.html',
    './t_app/public/**/*.js',
    './t_app/public/**/*.css',
  ],
  theme: {
    extend: {
   
        spacing: {
          'md': 'var(--margin-md, 1rem)',
          'sm': 'var(--margin-sm, 0.5rem)',
          'lg': 'var(--margin-lg, 1.5rem)',
          'xs': 'var(--margin-xs, 0.25rem)',
          'padding-md': 'var(--padding-md, 1rem)',
          'padding-sm': 'var(--padding-sm, 0.5rem)',
          'padding-lg': 'var(--padding-lg, 1.5rem)',
          'padding-xs': 'var(--padding-xs, 0.25rem)',
        },
        colors: {
          'fg': 'var(--fg-color, #fff)',
          'primary': '#ff6b6b', // Vibrant coral
          'secondary': '#4ecdc4', // Bright turquoise
          'accent': '#ffd93d', // Sunny yellow
          'dark': '#1a535c', // Deep teal
          'success': '#a8e6cf', // Mint green
          'warning': '#ffaaa5', // Soft peach
          'gradient-start': '#ff8c94', // Pink gradient start
          'gradient-end': '#ffedbc', // Light yellow gradient end
        },
        borderRadius: {
          'md': 'var(--border-radius-md, 0.375rem)',
          'sm': 'var(--border-radius-sm, 0.25rem)',
        },
        boxShadow: {
          'base': '0 4px 6px rgba(0,0,0,0.1)',
          'glow': '0 0 10px rgba(255,107,107,0.5)',
        },
        fontSize: {
          'sm': 'var(--text-sm, 0.875rem)',
          'md': 'var(--text-md, 1rem)',
          'base': 'var(--text-base, 1rem)',
          'lg': 'var(--text-lg, 1.125rem)',
          '2xl': 'var(--text-2xl, 1.5rem)',
          '3xl': 'var(--text-3xl, 1.875rem)',
        },
        scale: {
          '102': '1.02',
        },
        backgroundImage: {
          'gradient-primary': 'linear-gradient(135deg, #ff8c94, #ffedbc)',
        },
      },
    },
    plugins: [],
};

