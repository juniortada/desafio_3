# Author: Junior Tada
from app import app

# Roda Servidor Werkzeug
app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)