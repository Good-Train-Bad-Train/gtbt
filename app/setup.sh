# mkdir -p ~/.streamlit/

# mkdir -p ~/.streamlit/
# echo "[theme]
# primaryColor='#E55635'
# backgroundColor='#000000'
# secondaryBackgroundColor='#586e75'
# textColor='#fafafa'
# font='sans serif'


# echo "\
# [general]\n\
# email = \"your-email@domain.com\"\n\
# " > ~/.streamlit/credentials.toml

# echo "\
# [server]\n\
# headless = true\n\
# enableCORS=false\n\
# port = $PORT\n\
# " > ~/.streamlit/config.toml

mkdir -p ~/.streamlit/

echo "[theme]
primaryColor='#E55635'
backgroundColor='#000000'
secondaryBackgroundColor='#586e75'
textColor='#fafafa'
font='sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml