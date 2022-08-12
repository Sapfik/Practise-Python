const path = require(`path`);

const Dir = {
  ROOT: path.resolve(__dirname, `..`),
  WEBPACK: `webpack`,
  PLUGINS: `plugins`,
  GULP: `gulp`,
  TASKS: `tasks`,
};

const pathes = {
  webpack: {
    plugins: path.join(Dir.ROOT, Dir.WEBPACK, Dir.PLUGINS),
    config: path.join(Dir.ROOT, Dir.WEBPACK, `webpack.config.js`)
  },
  gulp: {
    tasks: path.join(Dir.ROOT, Dir.GULP, Dir.TASKS)
  }
};

const ServerType = {
  DEVELOPMENT: `DEVELOPMENT`,
  PRODUCTION: `PRODUCTION`
};

const currentServerType = ServerType.PRODUCTION;

module.exports = {Dir, pathes, ServerType, currentServerType};
