const _ = require('lodash');
const { hashStr, StrHash} = require("./common");

const resultsCache = require("./cache");

class ValueList {
    constructor() {
        this.values = [];
        this.cache = {};
        // this._hash = new StrHash();
    }
    
    add(value) {
        // let newHash = hashStr(String(value));
        this.values.push(value);
        // this._hash.combine(new StrHash(value));
    }
    
    // get hash() {
    //     return this._hash.valueOf();
    // }
    
    getTransformedValuesCB(transformerChain, includeTransient, cb, doneCb) {
        return transformerChain(this.values, cb, doneCb, this.cache, includeTransient);
    }
    
    // *getTransformedValues(transformerChain, includeTransient) {
    //     if (!transformerChain) {
    //         yield *this.values.map((v)=>[v,v]);
    //     } else {
    //         yield *transformerChain(this.values, this.cache, includeTransient);
    //     }
    // }
}

class DataFrame {
    constructor(ruleset) {
        this.dataMap = {};
        this.ruleset = ruleset;
    }
    
    // *addAndCheck(targetName, ...values) {
    //     let valueList = this.dataMap[targetName] = (this.dataMap[targetName] || new ValueList());
    //     values.forEach(v=>valueList.add(v));

    //     if (this.ruleset) {
    //         yield* this.ruleset.checkTarget(targetName, valueList); 
    //     }
    // }
    
    addAndCheckCB(targetName, cb, doneCB, ...values) {
        let valueList = this.dataMap[targetName] = (this.dataMap[targetName] || new ValueList());
        values.forEach(v=>valueList.add(v)); // TODO: can the be made faster using some sort of extend?

        if (this.ruleset) {
            this.ruleset.checkTargetCB(targetName, valueList, cb, doneCB); 
        }
    }
    
    async addAndCheckPromise(targetName, ...values) {
        let findings = [];
        return new Promise((resolve, reject)=>{
            this.addAndCheckCB(targetName, f=>findings.push(f), ()=>resolve(findings), ...values);
        });
    }
    // *getAll(key, transformerChain, includeTransient) {
    //     includeTransient = includeTransient || false;
    //     const valueList = this.dataMap[key];
    //     if (valueList) {
    //         yield *this._getTransformedValues(valueList, transformerChain, includeTransient)
    //     }
    // }
}

module.exports = DataFrame;