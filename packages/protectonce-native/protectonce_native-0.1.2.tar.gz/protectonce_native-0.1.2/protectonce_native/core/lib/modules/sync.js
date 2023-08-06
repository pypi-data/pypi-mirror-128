const Config = require('../utils/config');
const Constants = require('../utils/constants');
const ReportCache = require('../reports/reports_cache');
const RestAPI = require('../backend/restAPI');
const RulesManager = require('../rules/rules_manager');

function syncRules() {
    return new Promise((resolve, reject) => {
        const heartbeatInfo = {};
        heartbeatInfo[Constants.HEARTBEAT_HASH_KEY] = RulesManager.hash;
        heartbeatInfo[Constants.HEARTBEAT_REPORT_KEY] = ReportCache.flush();

        const restApi = new RestAPI(Constants.REST_API_HEART_BEAT, heartbeatInfo);
        restApi.post().then((rules) => {
            RulesManager.handleIncomingRules(rules);
            resolve(RulesManager.runtimeRules);
        }).catch((e) => {
            console.log(`syncRules failed with error: ${e}`);
            reject(e);
        })
    });
}

// Send heartbeat every n seconds as defined by Config.syncInterval
setInterval(syncRules, Config.syncInterval).unref();
