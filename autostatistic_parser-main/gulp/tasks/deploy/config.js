const path = require(`path`);
const {pathes, ServerType, currentServerType} = require(`./../../config.js`);

const rsyncConfig = {
  archive: true,
  silent: false,
  incremental: true
};
let srcPath;

switch (currentServerType) {
  case ServerType.PRODUCTION:
    rsyncConfig.hostname = `auto_ru_scrapper@109.68.215.2`;
    rsyncConfig.destination = '/home/auto_ru_scrapper/auto_ru_scrapper/scrapper/';
    rsyncConfig.archive = false;
    rsyncConfig.silent = false;
    rsyncConfig.compress = true;
    rsyncConfig.exclude = [
      'configs/platform_config.py',
      'notes/**/*'
    ];
    srcPath = [
      '@(bash|auto_ru|webdrivers|configs|modules|utils|service|checks|clean_up)/**/*',
      'venv/lib/python3.8/site-packages/module-pathes.pth',
      '!**/__pycache__/**/*'
    ];
    break;
}

module.exports = {srcPath, rsyncConfig};
