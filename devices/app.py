import config

connex_app = config.connex_app
connex_app.add_api('openapi.yaml')

if __name__ == '__main__':
    connex_app.run(debug=True)