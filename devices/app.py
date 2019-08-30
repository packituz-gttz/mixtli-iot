from devices import config

connex_app = config.connex_app
# Load api specification
connex_app.add_api('openapi.yaml')

if __name__ == '__main__':
    connex_app.run(debug=True)