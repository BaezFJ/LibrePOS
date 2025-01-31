const defaultTheme = 'dark'
const theme = localStorage.getItem('theme');
if (theme) document.documentElement.setAttribute('theme', theme);
else document.documentElement.setAttribute('theme', defaultTheme);