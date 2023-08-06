const RuleSet = require("./ruleset");
const Metrics = require("./metrics");
const DataFrame = require("./dataFrame");

class WAF {
    constructor (ruleSetDef, context) {
        this.context = context || {};
        this.metrics = this.context.metrics = this.context.metrics || new Metrics();
        
        this.ruleset = new RuleSet(ruleSetDef, this.context);
    }
    
    createDataFrame() {
        return new DataFrame(this.ruleset);
    }
}

WAF.DataFrame = DataFrame;

module.exports = WAF;