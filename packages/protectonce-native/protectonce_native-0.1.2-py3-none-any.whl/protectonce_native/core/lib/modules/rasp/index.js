const _ = require('lodash');

const openRASP = require('./openRASP');
const ProtectOnceContext = require('../context');
const RegExpManager = require('../../utils/regex_manager');
const Report = require('../../reports/report');
const ReportsCache = require('../../reports/reports_cache');
const RulesManager = require('../../rules/rules_manager');
const { RuntimeData } = require('../../runtime/runtime_data');
const { SQLData } = require('../../runtime/runtime_data');

function checkRegexp(data) {
    return Promise.resolve()
        .then(() => {
            const runtimeData = new RuntimeData(data);
            const rule = RulesManager.getRule(runtimeData.context);

            if (!rule) {
                return runtimeData;
            }

            const regExpressions = rule.regExps;
            let match = false;
            const args = runtimeData.args;
            for (let regExpId of regExpressions) {
                const regExp = RegExpManager.getRegExp(regExpId);

                // TODO: Use args from the rule instead of scanning all args
                for (let arg of args) {
                    // FIXME: What about arguments which are other than string
                    if (!_.isString(arg)) {
                        continue;
                    }

                    if (arg.search(regExp) >= 0) {
                        match = true;
                        break;
                    }
                }

                if (match === true) {
                    break;
                }
            }

            if (match) {
                let reportType = Report.ReportType.REPORT_TYPE_ALERT;
                runtimeData.message = 'ProtectOnce has detected an attack';

                if (rule.shouldBlock === true) {
                    runtimeData.setBlock();
                    reportType = Report.ReportType.REPORT_TYPE_BLOCK;
                    runtimeData.message = 'ProtectOnce has blocked an attack'
                } else {
                    runtimeData.setAlert();
                }

                const report = new Report.Report(reportType, runtimeData.message);
                ReportsCache.cache(report);
            }

            return runtimeData;
        });
}

function detectSQLi(data) {
    return Promise.resolve().then(() => {
        const sqlData = new SQLData(data.data);

        const rule = RulesManager.getRule(data.context);
        if (!rule) {
            return sqlData;
        }

        const context = ProtectOnceContext.get(sqlData.sessionId);
        const result = openRASP.detectSQLi(sqlData.query, sqlData.callStack, context);
        if (!result) {
            return sqlData;
        }

        let reportType = Report.ReportType.REPORT_TYPE_ALERT;
        if (rule.shouldBlock === true) {
            sqlData.setBlock();
            reportType = Report.ReportType.REPORT_TYPE_BLOCK;
        } else {
            sqlData.setAlert();
        }
        const report = new Report.Report(rule.id, result.name, result.severity, context.sourceIP, result.message, result.name, context.path);
        ReportsCache.cache(report);

        return sqlData;
    });
}

module.exports = {
    checkRegexp: checkRegexp,
    detectSQLi: detectSQLi
};
