const _ = require('lodash');

const Rule = require('./rule');

class RulesManager {
    constructor() {
        this._rules = {};
        this._hash = '';
    }

    get rules() {
        return Object.values(this._rules);
    }

    get hash() {
        return this._hash;
    }

    getRule(id) {
        const rule = this._rules[id];
        if (rule && rule.isEnabled) {
            return rule;
        }

        return null;
    }

    get runtimeRules() {
        // TODO: Optimise the runtime rules
        const runtimeRules = [];
        this.rules.forEach(rule => {
            runtimeRules.push(rule.runtimeRule);
        });
        return runtimeRules;
    }

    set rules(rules) {
        if (!_.isArray(rules) || rules.length === 0) {
            // Do not update rules if no rules are returned from backend
            return;
        }

        // TODO: Need to have optimized rules storage once backend starts sending rules diff
        this._rules = {};
        for (let rule of rules) {
            const ruleObj = new Rule(rule);
            this._rules[rule.id] = ruleObj;
        }
    }

    handleIncomingRules(rules) {
        const rulesJson = JSON.parse(rules);
        const agentRule = rulesJson.agentRule;

        if (typeof agentRule === 'undefined' || !_.isObject(agentRule)) {
            return;
        }
        this._hash = agentRule.hash || '';
        this.rules = agentRule.hooks || [];
    }
}

module.exports = new RulesManager();
