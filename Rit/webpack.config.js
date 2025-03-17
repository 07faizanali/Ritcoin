const path = require('path');
const webpack = require('webpack'); // Add this line


module.exports = {
    entry: '/static/js/web3modal.js',  // Replace with your entry file path
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'static/dist'),  // Replace with your output directory
    },
    resolve: {
        fallback: {
            "stream": require.resolve("stream-browserify"),
            "http": require.resolve("stream-http"),
            "https": require.resolve("https-browserify"),
            "os": require.resolve("os-browserify/browser"),
            "buffer": require.resolve("buffer")
        },
        extensions: ['.js', '.jsx'], // Add support for .jsx files
    },
    module: {
        rules: [
            {
                //test: /\.m?js$/,
                test: /\.(js|jsx)$/, // Add support for JSX syntax
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        // presets: ['@babel/preset-env']
                        presets: [
                            '@babel/preset-env',
                            '@babel/preset-react', // Add React preset to handle JSX
                          ],
                    }
                }
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            Buffer: ['buffer', 'Buffer'],
        }),
    ],
};
