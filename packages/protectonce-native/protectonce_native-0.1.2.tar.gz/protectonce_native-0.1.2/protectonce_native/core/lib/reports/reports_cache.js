class ReportCache {
    constructor() {
        this._cache = [];
    }

    cache(report) {
        this._cache.push(report);
    }

    flush() {
        const reports = this._cache;
        this._cache = [];
        return reports;
    }
}

module.exports = new ReportCache();
