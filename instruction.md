There is an Apache-style access log at `/app/access.log` in the working directory.
Analyze the traffic and write a JSON summary to `/app/report.json`.

The report is a single JSON object with exactly these three keys:

- `total_requests`: number of requests (non-empty lines) in the log.
- `unique_ips`: number of distinct client IP addresses (the first whitespace-separated
  field of each line).
- `top_path`: the request path (the target of the HTTP request line, e.g.
  `/index.html`) that appears in the most requests.

Your report is correct when:

1. `/app/report.json` exists and contains valid JSON.
2. The JSON is an object whose keys are exactly `total_requests`, `unique_ips`, and
   `top_path`, with `total_requests` and `unique_ips` as integers and `top_path` as a string.
3. `total_requests` equals the number of requests in the log.
4. `unique_ips` equals the number of distinct client IP addresses in the log.
5. `top_path` equals the path that appears in the most requests.
