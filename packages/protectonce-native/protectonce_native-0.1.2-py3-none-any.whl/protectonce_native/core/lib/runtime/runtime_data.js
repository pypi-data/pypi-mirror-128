const RuntimeAction = {
    RUNTIME_ACTION_NONE: 'none',
    RUNTIME_ACTION_ALERT: 'alert',
    RUNTIME_ACTION_BLOCK: 'block'
};

class RuntimeData {
    constructor(runtimeData) {
        this.args = runtimeData.args || [];
        this.context = runtimeData.context || '';
        this.action = RuntimeAction.RUNTIME_ACTION_NONE;
        this.message = runtimeData.message || '';
        this.result = runtimeData.result || null;
        this.modifyArgs = runtimeData.modifyArgs || {};
        this.callStack = runtimeData.callStack || [];
    }

    setBlock() {
        this.action = RuntimeAction.RUNTIME_ACTION_BLOCK;
    }

    setAlert() {
        this.action = RuntimeAction.RUNTIME_ACTION_ALERT;
    }
}

class RASPData extends RuntimeData {
    constructor(raspData) {
        super(raspData);
        this.confidence = 0;
        this.sessionId = raspData.poSessionId || '';
    }
}

class SQLData extends RASPData {
    constructor(sqlData) {
        super(sqlData)
        this.query = sqlData.query;
    }

    get params() {
        return {
            'query': this.query,
            'stack': this.callStack
        };
    }
}

module.exports = {
    RuntimeData: RuntimeData,
    SQLData: SQLData
};
