import os
from flask import Flask
from diary.settings import ProdConfig
from diary.assets import assets
from diary import controller
from flask_stormpath import StormpathError, StormpathManager, User, login_required, login_user, logout_user, user

def create_app(config_object=ProdConfig):
    diary = Flask(__name__.split('.')[0])
    diary.config.from_object(config_object)
    print(config_object)
    #diary.error_handler_spec[None][404] = not_found
    #diary.error_handler_spec[None][500] = server_error
    register_extensions(diary)
    register_logger(diary)
    register_database(diary)
    register_stormpath(diary)
    register_blueprints(diary)
    register_errorhandlers(diary)
    return diary

def register_extensions(diary):
    assets.init_app(diary)

def register_logger(diary):
    from diary.logger import Log
    log_filepath = os.path.join(diary.root_path,
                   diary.config['LOG_FILE_PATH'])
    print(log_filepath)
    Log.init(log_filepath=log_filepath)

def register_database(diary):
    from diary.database import DBManager
    db_filepath = os.path.join(diary.root_path, 
                               diary.config['DB_FILE_PATH'])
    db_url = diary.config['DB_URL'] + db_filepath
    print(db_url)
    DBManager.init(db_url, eval(diary.config['DB_LOG_FLAG']))    
    DBManager.init_db()

def register_stormpath(diary):
    diary.config['DEBUG'] = True
    diary.config['SECRET_KEY'] = '3WotnDW3JOwjnkXWnmot/yX6dKgQSDHDWAEPHW5a5F8'
    diary.config['STORMPATH_API_KEY_FILE']='apiKey.properties'
    diary.config['STORMPATH_APPLICATION']='Diary'
    diary.config['STORMPATH_ENABLE_LOGIN'] = True
    diary.config['STORMPATH_ENABLE_REGISTRATION'] = True
    diary.config['STORMPATH_ENABLE_LOGOUT'] = True
    stormpath_manager = StormpathManager(diary)
    return None

def register_errorhandlers(diary):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        diary.errorhandler(errcode)(render_error)
    return None


def register_blueprints(diary):
    """Register Flask blueprints."""
    diary.register_blueprint(controller.app.blueprint)
    return None

def not_found(error):
    return render_template('404.html'), 404

def server_error(error):
    err_msg = str(error)
    return render_template('500.html', err_msg=err_msg), 500
