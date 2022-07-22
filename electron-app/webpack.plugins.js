const ForkTsCheckerWebpackPlugin = require("fork-ts-checker-webpack-plugin");
// Required tp resolve this issue:
// https://stackoverflow.com/questions/64557638/how-to-polyfill-node-core-modules-in-webpack-5
//const NodePolyfillPlugin = require('node-polyfill-webpack-plugin');

module.exports = [
  new ForkTsCheckerWebpackPlugin(),
  // new NodePolyfillPlugin()
];
