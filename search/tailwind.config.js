const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    './components/**/*.{html,js,ts,jsx,tsx}',
    './pages/**/*.{html,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        wellcome: ['Wellcome'],
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
      },
      colors: {
        red: '#C88F7E',
        tan: '#E6B692',
        blue: '#729CB2',
        pink: '#E0B3BF',
        green: '#AAAA81',
        yellow: '#DFD76E',
        black: '#131313',
        brown: '#C7A879',
        paper: { 1: '#FBF6E9', 2: '#F0EADA', 3: '#DED5BF' },
        white: '#FFFFFF',
      },
      spacing: {
        '1/2': '50%',
        '2/3': '66.666667%',
        '3/4': '75%',
        '4/5': '80%',
      },
    },
  },
}
