class ProtectOnceContext {
    static _contextMap = {};

    static create(id, context) {
        this._contextMap[id] = context;
    }

    static update(id, context) {
        if (!this._contextMap[id]) {
            this._contextMap[id] = context;
            return;
        }

        this._contextMap[id] = {
            ...this._contextMap[id],
            ...context
        };
    }

    static release(id) {
        const context = this._contextMap[id];
        delete this._contextMap[id];
        return context;
    }

    static get(id) {
        return this._contextMap[id];
    }
}

module.exports = ProtectOnceContext;
