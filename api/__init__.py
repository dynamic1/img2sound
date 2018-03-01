from flask import Flask, Blueprint, send_from_directory
from flask_restful import Api

from api.controllers import spectrogram

from config import config
import os.path

def create_app(env):

    app = Flask(__name__)
    app.config.from_object(config[env])
    app.config['PROJECT_ROOT_PATH'] = os.path.abspath(os.path.join(app.root_path, '../'))
    app.config.storage_path = os.path.abspath(os.path.join(app.root_path, '../storage/'))
    app.config.uploads_path = os.path.join(app.config.storage_path, app.config['UPLOADS_FOLDER'])
    app.config.spectrograms_path = os.path.join(app.config.storage_path, app.config['SPECTROGRAMS_FOLDER'])
    
    # index.html will be serverd from WEB_PATH 
    app.config['WEB_PATH'] = os.path.join(app.config['PROJECT_ROOT_PATH'], 'web')
    # /dist files will be server from WEB_DIST_PATH
    app.config['WEB_DIST_PATH'] = os.path.join(app.config['WEB_PATH'], 'dist')

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    api.add_resource(spectrogram.CreateSpectrogram, '/spectrogram')

    app.register_blueprint(api_bp, url_prefix='/api/v1')


    @app.route('/uploads/<filename>')
    def storage_uploads(filename):
        # print(f"storage_path: {app.config.storage_path}")
        selected_storage = app.config.uploads_path
        print(f"sending {filename} from {selected_storage}")
        return send_from_directory(selected_storage, filename)

    @app.route('/spectrograms/<filename>')
    def storage_spectrograms(filename):
        # print(f"storage_path: {app.config.storage_path}")
        selected_storage = app.config.spectrograms_path
        print(f"sending {filename} from {selected_storage}")
        return send_from_directory(selected_storage, filename)

    @app.after_request # blueprint can also be app
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        return response

    @app.route('/dist/<filename>')
    def web_dist(filename):
        selected_storage = app.config['WEB_DIST_PATH']
        print(f"sending {filename} from {selected_storage}")
        return send_from_directory(selected_storage, filename)


    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        path = path or 'index.html'
        print(f"project_path = {app.config['PROJECT_ROOT_PATH']}")
        print(f"web_path = {app.config['WEB_PATH']}")
        print(f"web_dist_path = {app.config['WEB_DIST_PATH']}")
        
        selected_storage = app.config['WEB_PATH']
        print(f"sending {path} from {selected_storage}")
        return send_from_directory(selected_storage, path)
    
    return app