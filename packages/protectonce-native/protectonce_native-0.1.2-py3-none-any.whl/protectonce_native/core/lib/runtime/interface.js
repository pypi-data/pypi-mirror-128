const login = require('../modules/login');
const rasp = require('../modules/rasp');
const httpServer = require('../modules/httpServer');
require('../modules/sync');

function stop() {
    // TODO: Implement this method and add cleanup if any
    return Promise.resolve();
}

function sync() {
    // TODO: Implement this method
    return Promise.resolve();
}

module.exports = {
    init: login,
    sync: sync,
    rasp: rasp,
    httpServer: httpServer,
    stop: stop
};
