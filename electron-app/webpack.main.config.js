module.exports = {
  /**
   * This is the main entry point for your application, it's the first file
   * that runs in the main process.
   */
  entry: "./src/electron-main.ts",
  // Put your normal webpack config below here
  module: {
    rules: require("./webpack.rules"),
  },
  resolve: {
    extensions: [
      ".js",
      ".ts",
      ".jsx",
      ".tsx",
      ".css",
      ".json",
      ".scss",
      ".sass",
    ],
    // fallback: {
    //   "path": require.resolve("path-browserify"),
    //   "os": require.resolve("os-browserify/browser"),
    //   "stream": require.resolve("stream-browserify"),
    //   "assert": require.resolve("assert/"),
    //   "url": require.resolve("url/"),
    //
    //   "path": false,
    //   "os": false,
    //   "stream": false,
    //   "assert": false,
    //   "url": false,
    // }
  }
};
