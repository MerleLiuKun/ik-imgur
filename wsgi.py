from app import create_app

import config
from app.extensions import init_db

app = create_app()


@app.listener('before_server_start')
async def setup_db(app, loop):
    await init_db()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=config.DEBUG, auto_reload=False)
