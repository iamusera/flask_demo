from application import create_app

app = create_app()

import dask
dask.config.set(scheduler='threads')
print('dask setting')

if __name__ == '__main__':
    app.run(debug=True)
