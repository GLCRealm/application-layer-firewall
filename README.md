
# Application-Layer Firewall in Python

This project is an **Application-Layer Firewall** built with Flask. It is designed to detect and block malicious activities such as **SQL injection**, **Cross-Site Scripting (XSS)**, and **excessive requests** (rate-limiting) at the application level.

## Features
- **SQL Injection Detection**: Identifies and blocks common SQL injection patterns in incoming requests.
- **XSS Protection**: Detects and blocks potential Cross-Site Scripting (XSS) attacks.
- **Rate Limiting**: Limits the number of requests per minute from the same IP to prevent DoS attacks.
- **Logging**: Logs all blocked requests with details such as the IP address and reason for blocking.

---

## How It Works
1. Incoming requests are analyzed for malicious patterns using regex-based rules.
2. If a request matches:
   - **SQL Injection Pattern**: The request is blocked with a `403 Forbidden` response.
   - **XSS Pattern**: The request is blocked with a `403 Forbidden` response.
   - **Rate Limit Exceeded**: The request is blocked with a `429 Too Many Requests` response.
3. Blocked requests are logged into `malicious_requests.log` for further analysis.

---

## Installation and Usage

### Prerequisites
- Python 3.6 or higher
- Flask library

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/application-layer-firewall.git
   cd application-layer-firewall
   ```

2. Install dependencies:
   ```bash
   pip install flask
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. Access the application at:
   ```
   http://127.0.0.1:5000/
   ```

---

## Testing the Firewall

### SQL Injection Test
- URL Example:
  ```
  http://127.0.0.1:5000/?username=admin' OR 1=1 --
  ```
- Expected Response: `403 Forbidden`.

### XSS Test
- URL Example:
  ```
  http://127.0.0.1:5000/?q=<script>alert('XSS')</script>
  ```
- Expected Response: `403 Forbidden`.

### Rate-Limiting Test
- Send more than 20 requests in one minute from the same IP.
- Expected Response: `429 Too Many Requests`.

### Logs
- All blocked requests are logged in `malicious_requests.log`.

---

## File Structure
```
application-layer-firewall/
│
├── main.py                 # Core Flask application
├── malicious_requests.log  # Log file for blocked requests
├── README.md               # Documentation (this file)
```

---

## Future Improvements
- Support for more attack types like CSRF and file upload scanning.
- Machine learning-based detection for advanced threat identification.
- Dashboard for monitoring requests and logs.



