from pyramid.paster import get_app
from waitress import serve

appIniPath = 'development.ini'

app = get_app(appIniPath)

serve(app, host="0.0.0.0", port=8080)
