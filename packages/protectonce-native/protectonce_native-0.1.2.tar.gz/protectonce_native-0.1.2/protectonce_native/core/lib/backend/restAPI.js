const https = require('https');
const Constants = require('../utils/constants');

const BackendConfig = require('./config');
const Token = require('./token');

class RestAPI {
    constructor(path, data) {
        this._path = path;
        try {
            this._data = JSON.stringify(data);
        } catch (e) {
            this._data = '';
        }
    }

    get url() {
        return BackendConfig.endpoint;
    }

    get port() {
        return BackendConfig.port;
    }

    get postOptions() {
        const postOpts = {
            hostname: this.url,
            path: this._path,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': this._data.length,
                'Authorization': Token.authHeader
            }
        };

        if (this.port) {
            postOpts['port'] = this.port;
        }

        if (Token.refreshToken) {
            postOpts.headers[Constants.BACKEND_REST_API_REFRESH_TOKEN_HEADER] = Token.refreshToken
        }

        return postOpts;
    }

    post() {
        return new Promise((resolve, reject) => {
            const req = https.request(this.postOptions, res => {
                let data = '';
                res.on('data', d => {
                    data += d.toString();
                })

                res.on('end', () => {
                    const responseObj = JSON.parse(data);
                    const authDetails = responseObj['authDetails'];
                    if (authDetails) {
                        Token.update(authDetails);
                    }
                    resolve(JSON.stringify(responseObj));
                });
            })

            req.on('error', error => {
                console.error(error);
                reject(error);
            })

            req.write(this._data)
            req.end()
        });
    }
}

module.exports = RestAPI;
