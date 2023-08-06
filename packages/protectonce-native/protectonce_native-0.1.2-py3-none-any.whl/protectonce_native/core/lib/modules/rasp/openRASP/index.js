const _ = require('lodash');

require('./init')();

const Severity = {
    OPEN_RASP_SEVERITY_MINOR: 'minor',
    OPEN_RASP_SEVERITY_MAJOR: 'major',
    OPEN_RASP_SEVERITY_CRITICAL: 'critical'
};

function _toRASPQueryParams(queryParams) {
    Object.keys(queryParams).forEach(key => {
        if (_.isString(queryParams[key])) {
            // open rasp expects each parameter to be an array of strings
            queryParams[key] = [queryParams[key]];
        }
    })
    return queryParams;
}

function _toOpenRASPContext(context) {
    // TODO: Add json data as well
    return {
        'header': context['headers'] || {},
        'parameter': _toRASPQueryParams(context['queryParams'] || {}),
    }
}

// FIXME: Need to move this to backend. Agent should report confidence instead
function _getSeverity(result) {
    const confidence = result['confidence'] || 0;
    if (confidence <= 60) {
        return Severity.OPEN_RASP_SEVERITY_MINOR;
    }

    if (confidence <= 90) {
        return Severity.OPEN_RASP_SEVERITY_MAJOR;
    }

    return Severity.OPEN_RASP_SEVERITY_CRITICAL;
}

/* expects context of the form:
 *  {
 *      "headers": {<key value pair of headers>},
 *      "queryParams": {<key value pair of query parameters>},
 *  }
*/
function detectSQLi(query, callStack, context) {
    const results = RASP.check('sql', {
        query: query,
        stack: callStack || []
    }, _toOpenRASPContext(context));

    if (results.length === 0) {
        return null;
    }

    return {
        'name': results[0].algorithm || '',
        'message': results[0].message || '',
        'severity': _getSeverity(results[0])
    }
}


module.exports = {
    detectSQLi: detectSQLi
};
