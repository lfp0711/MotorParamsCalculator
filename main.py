
from config import config
from flask import Flask, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import  CSRFProtect
from calculator import bp

import logging

app = Flask(__name__)
app.config.from_object(config['Development'])
config['Development'].init_app(app)

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

app.register_blueprint(bp)
app.json.ensure_ascii = False

print(app.url_map)

# 配置日志
logging.basicConfig(filename='motor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info('Started')
    app.run(debug=True, host='0.0.0.0')

