module.exports = {
  purge: [
    './components/**/*.{html,js,ts,jsx,tsx}',
    './pages/**/*.{html,js,ts,jsx,tsx}',
  ],
  darkMode: false,
  theme: {
    extend: {
      spacing: { '2/3': '66.666667%' },
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
      },
    },
  },
}
