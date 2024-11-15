from flask import Flask, request, abort
import re
import logging
import time

app = Flask(__name__)

# logging  
logging.basicConfig(filename='malicious_requests.log', level=logging.INFO)

#  custom rule set
sql_injection_patterns = [
    r"(?:')|(?:--)|(/\*(?:.|[\\n\\r])*?\*/)|(?:\b(ALTER|CREATE|DELETE|DROP|EXEC|INSERT|MERGE|SELECT|UPDATE|UNION|USE)\b)"
]
xss_patterns = [
    r"(<script.*?>.*?</script>)|(<.*?onerror=.*?>)|(<.*?onload=.*?>)"
]
rate_limit = {}
MAX_REQUESTS_PER_MINUTE = 20

# Function to log a malicious request
def log_malicious_request(request, reason):
    logging.info(f"Blocked request from {request.remote_addr} for reason: {reason}")
    print(f"Blocked request from {request.remote_addr} for reason: {reason}")

# middleware to check for malicious patterns
@app.before_request
def check_request():
     
    ip = request.remote_addr
    if ip not in rate_limit:
        rate_limit[ip] = [0, time.time()]  # [count, timestamp]

    count, start_time = rate_limit[ip]
    if time.time() - start_time < 60:
        rate_limit[ip][0] += 1
    else:
        rate_limit[ip] = [1, time.time()]

    if rate_limit[ip][0] > MAX_REQUESTS_PER_MINUTE:
        log_malicious_request(request, "Rate limit exceeded")
        abort(429)
    # SQL Injection check
    for pattern in sql_injection_patterns:
        if re.search(pattern, request.data.decode('utf-8')) or re.search(pattern, str(request.args)):
            log_malicious_request(request, "SQL Injection attempt")
            abort(403)

    # XSS check
    for pattern in xss_patterns:
        if re.search(pattern, request.data.decode('utf-8')) or re.search(pattern, str(request.args)):
            log_malicious_request(request, "XSS attempt")
            abort(403)

# Sample endpoint  
@app.route('/', methods=['GET', 'POST'])
def index():
    return "Welcome to the WAF-Protected Application"

if __name__ == '__main__':
    app.run(debug=True)
