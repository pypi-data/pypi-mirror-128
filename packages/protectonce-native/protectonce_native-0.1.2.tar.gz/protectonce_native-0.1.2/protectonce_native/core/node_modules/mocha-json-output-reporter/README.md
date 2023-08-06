# mocha-json-output-reporter
mocha spec + json output file reporter

Combines the spec and json reporter but instead of outputting the json to the console, writes it to a file

# Install
```
npm install --save-dev mocha-json-output-reporter
```

# Run with Mocha
```
mocha -R mocha-json-output-reporter
```

# Output file
The default file output will be `mocha-output-<date>` in the current working directory

## Reporter Options
* output - specify exact name of output file

```
mocha --reporter-options output=my-file.json
```

### Example Output - Default Mode
```
{
  "stats": {
    "suites": 3,
    "tests": 9,
    "passes": 9,
    "pending": 0,
    "failures": 0,
    "start": "2021-07-15T20:06:25.845Z",
    "end": "2021-07-15T20:06:27.489Z",
    "duration": 1644
  },
  "tests": [
    {
      "title": "should success registration with granted access",
      "fullTitle": "account invitation behaviour account invitation behaviour with the enabled access-policy should success registration with granted access",
      "file": "/tests/account.spec.js",
      "duration": 235,
      "currentRetry": 0,
      "err": {}
    },
    {
      "title": "success:becomeMemberByInvitationCode",
      "fullTitle": "account invitation behaviour account invitation behaviour with the enabled access-policy success:becomeMemberByInvitationCode",
      "file": "/tests/account.spec.js",
      "duration": 63,
      "currentRetry": 0,
      "err": {}
    },
    {
      "title": "failed:becomeMemberByInvitationCode:invalidInviteToken:wrongUser ",
      "fullTitle": "account invitation behaviour account invitation behaviour with the enabled access-policy failed:becomeMemberByInvitationCode:invalidInviteToken:wrongUser ",
      "file": "/tests/account.spec.js",
      "duration": 18,
      "currentRetry": 0,
      "err": {}
    }
  ]
}
```
