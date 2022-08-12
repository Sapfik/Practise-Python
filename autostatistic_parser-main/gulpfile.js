const {series, parallel, watch} = require(`gulp`);

const path = require(`path`);
const {pathes} = require(`./gulp/config.js`);

const deploy = require(path.join(pathes.gulp.tasks, `deploy/task.js`));

module.exports.deploy = deploy;
