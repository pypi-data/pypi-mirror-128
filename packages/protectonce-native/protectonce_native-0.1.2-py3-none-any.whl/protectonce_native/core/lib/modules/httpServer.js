const uuid = require('uuid');
const ProtectOnceContext = require('./context');

function createSession() {
    // TODO: This is a stopgap implementation of session id
    return Promise.resolve().then(() => {
        const sessionId = uuid.v4();
        ProtectOnceContext.create(sessionId, {});
        return sessionId;
    });
}

/**
 * Releases the stored http session, this should be called when a request is completed
 * @param  {Object} sessionData The incoming data is of the form:
 *          @param {Object} data This holds following field:
 *              @param {String} poSessionId
 */
function releaseSession(sessionData) {
    return Promise.resolve().then(() => {
        ProtectOnceContext.release(sessionData.data.poSessionId);
    });
}

/**
 * Stores the http request info in the session context
 * @param  {Object} requestData The incoming data is of the form:
 *          @param {Object} data This holds http request object of the form:
 *              @param {Object} queryParams
 *              @param {Object} headers
 *              @param {String} method
 *              @param {String} path
 *              @param {String} sourceIP
 *              @param {String} poSessionId
 */
function storeHttpRequestInfo(requestData) {
    return Promise.resolve().then(() => {
        ProtectOnceContext.update(requestData.data.poSessionId, requestData.data);
    });
}

function scanHeaders() {
    // TODO: Implement this
    return Promise.resolve().then(() => {
        return {
            'blocked': false
        }
    });
}

function scanHttpData() {
    // TODO: Not Implemented
    return Promise.resolve().then(() => {
        return {
            'blocked': false
        }
    });
}

module.exports = {
    createSession: createSession,
    releaseSession: releaseSession,
    storeHttpRequestInfo: storeHttpRequestInfo,
    scanHeaders: scanHeaders,
    scanHttpData: scanHttpData
};
