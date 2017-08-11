module.exports = {
    entry: './frontend/main.js',
    output: {
        path: __dirname + '/onepage/static',
        filename: 'bundle.js',
        publicPath: '/',
    },
    module: {
        loaders: [
            { test: /\.vue$/, loader: 'vue-loader' }
        ]
    }
}
