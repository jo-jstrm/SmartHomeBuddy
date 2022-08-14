const rules = require("./webpack.rules");
const plugins = require("./webpack.plugins");

rules.push({
  test: /\.css$/,
  use: [{ loader: "style-loader" }, { loader: "css-loader" }],
});

module.exports = {
  module: {
    rules,
  },
  plugins: plugins,
  resolve: {
    extensions: [".js", ".ts", ".jsx", ".tsx", ".css"],
    // fallback: {
    // "path": require.resolve("path-browserify"),
    // "os": require.resolve("os-browserify/browser"),
    // "stream": require.resolve("stream-browserify"),
    // "assert": require.resolve("assert/"),
    // "url": require.resolve("url/"),
    //
    // "path": false,
    // "os": false,
    // "stream": false,
    // "assert": false,
    // "url": false,
    // }
  },
};
