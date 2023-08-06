'use strict';

const addon = require('../../../../build/Release/po-openrasp-addon');

global.tokenize = function (query, type) {
    const result = []
    const arr = addon.flex_tokenize(query, type) || []
    for (let i = 0; i < arr.length; i += 2) {
        const start = arr[i]
        const stop = arr[i + 1]
        const text = query.substring(start, stop)
        result.push({ start, stop, text })
    }
    return result
}