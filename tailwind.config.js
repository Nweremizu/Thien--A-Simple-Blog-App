/** @type {import('tailwindcss').Config} */
module.exports = {
    mode: 'jit',
    content: ["./app/**/*.html", "./app/**/*.js"],
    theme: {
        extend: {
            screens: {
                sm: "640px",
                md: "768px",
                lg: "1024px",
                xl: "1280px",
                "1xl": "1440px",
                "2xl": "1536px",
                "3xl": "1920px",
            },
            colors: {
                primary: "#FEE58B",
                primary1:"#FEE58B",
				secondary1: "#353535",
				dark: "#28272C",
				light: "#f4f4f4",
				form_label: "#8c8c8c",
            },
            fontFamily: {
                sans: ["Roboto", "sans-serif"],
                serif: ["Roboto Slab", "serif"],
                mono: ["Roboto Mono", "monospace"],
            },
            boxShadow: {
                form: "5px 5px 0px #000000",
                small:"3px 3px 0px #000000",
            },
        },
    },
    plugins: [],
};

