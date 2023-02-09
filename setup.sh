mkdir -p ~/.streamlit/
echo "[theme]
base='light'
font = 'sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml