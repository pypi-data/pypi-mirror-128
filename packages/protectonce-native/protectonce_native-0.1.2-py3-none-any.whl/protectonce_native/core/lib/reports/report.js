class Report {
    constructor(id, name, severity, ipAddress, message, type, path) {
        this.id = id;
        this.name = name;
        this.severity = severity;
        this.ip_addresses = [ipAddress]; // TODO: How to get multiple IP addresses?
        this.security_response = message;
        this.date = new Date();
        this.type = type;
        this.request_path = path;
        this.report_type = "incident"; // TODO: What are other types?

        // FIXME: Currently it is same as date, may be once APM is integrated this might have different value
        this.date_started = new Date();
        this.request = 200; // TODO: Check what is this
        this.user = ""; // TODO: This will be done once user management is implemented,
        this.duration = 0; // TODO: What does this indicate?
    }
}

const ReportType = {
    'REPORT_TYPE_ALERT': 'report',
    'REPORT_TYPE_ALERT': 'alert',
    'REPORT_TYPE_BLOCK': 'block'
};

module.exports = {
    Report: Report,
    ReportType: ReportType
};
