module.exports = {
  future: {
      removeDeprecatedGapUtilities: true,
      purgeLayersByDefault: true,
  },
  purge: {
      enabled: false, //true for production build
      content: [
          '../**/templates/*.html',
          '../**/templates/**/*.html',
      ]
  },
  theme: {
      extend: {
        colors: {
        primary:'#2B2E4A',
        secondary: {
          100: '#E84545',
          200:'#903749',
          300:'#53354A',
          400:'#04293A',
          500:'#064663',
          600:'#ECB365',
          700:'#046832',
        },
        primary2:'#041C32',
      },
      fontFamily:{
        body:['Nunito'],
        secondary:['Roboto']
      },
      width:{
        800 : '800px'
      },
    },
  },
  variants: {},
  plugins: [],
}
