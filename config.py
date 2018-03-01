class Config(object):
    DEBUG = True
    TESTING = True


class DevelopmentConfig(Config):
    SECRET_KEY = "askdjfhads8kfjhasd",
    UPLOADS_FOLDER = "uploads"
    SPECTROGRAMS_FOLDER = "spectrograms"


config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig
}