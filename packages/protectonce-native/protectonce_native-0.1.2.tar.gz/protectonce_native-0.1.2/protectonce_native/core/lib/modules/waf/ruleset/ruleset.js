'use strict';

const Rule = require("./rule");
const Flow = require("./flow");
const TargetProcessor = require("./base");
const ResultCache = require("../cache");
const Metrics = require("../metrics");

class RuleSet extends TargetProcessor {
    
    constructor(ruleSetDef, context) {
        context = context || {};
        if (!context.metrics) {
            context.metrics = new Metrics();
        }
        context.cache = new ResultCache({ metrics: context.metrics });
        super(context, ruleSetDef.id || "");
        this.shouldCache = true;
        
        this.rules = (ruleSetDef.rules||[]).reduce((rules, ruleDef)=>{ let rule = new Rule(ruleDef, context); rules[rule.id]=rule; return rules;}, {});
        this.flows = (ruleSetDef.flows||[]).map(flowDef => new Flow(flowDef, this.rules, context));
        this.buildTargetMap(this.flows);        
    }

}

module.exports = RuleSet;
