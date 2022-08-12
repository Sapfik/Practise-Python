const {src} = require(`gulp`);
const gulpLoadPlugins = require(`gulp-load-plugins`)();

const {srcPath, rsyncConfig} = require(`./config.js`);

const deploy = () => {
  return src(srcPath)
    .pipe(gulpLoadPlugins.rsync(rsyncConfig));
};

module.exports = deploy;
