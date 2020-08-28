REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

}