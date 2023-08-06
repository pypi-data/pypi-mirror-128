const BaseFilter = require("../base")
var poAddon = require('../../../../../build/Release/po-addon');

class DetectXSSFilter extends BaseFilter {
    constructor(filterDef, context) {
        super(filterDef, "detectXSS", context);
    }

    doCheckCB(data, originalData, findingCb, doneCb) {
        let match = poAddon.detectXSS(data);
        if (match) {
            findingCb({
                data,
                originalData,
                pattern: this.pattern
            });
        }
        doneCb();
    }
};

module.exports = DetectXSSFilter;