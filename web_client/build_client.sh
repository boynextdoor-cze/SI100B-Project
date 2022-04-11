npm run build
rm -r -f ../web_server/static/
cp -r dist/static/ ../web_server/
cp dist/index.html ../web_server/templates