#!/usr/bin/env python3
"""Generate swagger-coverage HTML report and coverage.json from logged requests."""
import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None


def fetch_openapi_spec(base_url: str) -> dict | None:
    if requests is None:
        return None
    for path in ("/v3/api-docs", "/v2/api-docs", "/swagger-resources"):
        try:
            r = requests.get(f"{base_url}{path}", timeout=10)
            if r.ok:
                return r.json()
        except Exception:
            continue
    return None


def extract_spec_endpoints(spec: dict) -> list[dict]:
    endpoints = []
    paths = spec.get("paths", {})
    for path, methods in paths.items():
        for method in ("get", "post", "put", "patch", "delete", "head", "options"):
            if method in methods:
                summary = methods[method].get("summary", "")
                endpoints.append({"path": path, "method": method.upper(), "summary": summary})
    return endpoints


FALLBACK_SPEC_ENDPOINTS = [
    {"path": "/api/v1/admin/users", "method": "POST", "summary": "Create user (admin)"},
    {"path": "/api/v1/admin/users", "method": "GET", "summary": "Get all users (admin)"},
    {"path": "/api/v1/admin/users/{id}", "method": "DELETE", "summary": "Delete user (admin)"},
    {"path": "/api/v1/auth/login", "method": "POST", "summary": "Login"},
    {"path": "/api/v1/accounts", "method": "POST", "summary": "Create account"},
    {"path": "/api/v1/customer/accounts", "method": "GET", "summary": "Get customer accounts"},
    {"path": "/api/v1/customer/profile", "method": "GET", "summary": "Get customer profile"},
    {"path": "/api/v1/accounts/deposit", "method": "POST", "summary": "Deposit to account"},
    {"path": "/api/v1/accounts/transfer", "method": "POST", "summary": "Transfer between accounts"},
    {"path": "/api/v1/accounts/transfer-with-fraud-check", "method": "POST", "summary": "Transfer with fraud check"},
    {"path": "/api/v1/admin/users/{id}", "method": "GET", "summary": "Get user by ID (admin)"},
    {"path": "/api/v1/admin/users/{id}", "method": "PUT", "summary": "Update user (admin)"},
    {"path": "/api/v1/accounts/{id}", "method": "GET", "summary": "Get account by ID"},
    {"path": "/api/v1/accounts/{id}", "method": "DELETE", "summary": "Delete account"},
    {"path": "/api/v1/customer/profile", "method": "PUT", "summary": "Update customer profile"},
]


def load_logged_requests(input_dir: str) -> list[dict]:
    records = []
    if not os.path.isdir(input_dir):
        return records
    for fname in os.listdir(input_dir):
        if not fname.endswith(".json"):
            continue
        try:
            with open(os.path.join(input_dir, fname)) as f:
                records.append(json.load(f))
        except Exception:
            continue
    return records


def compute_coverage(spec_endpoints: list[dict], logged: list[dict]) -> dict:
    hit_set = set()
    status_map = defaultdict(set)
    for rec in logged:
        key = (rec["path"], rec["method"])
        hit_set.add(key)
        status_map[key].add(rec.get("status_code", 0))

    details = []
    for ep in spec_endpoints:
        key = (ep["path"], ep["method"])
        covered = key in hit_set
        statuses = sorted(status_map.get(key, []))
        details.append({
            "path": ep["path"],
            "method": ep["method"],
            "summary": ep.get("summary", ""),
            "covered": covered,
            "statuses": statuses,
        })

    total = len(spec_endpoints)
    covered = sum(1 for d in details if d["covered"])
    pct = round((covered / total) * 100, 2) if total > 0 else 0.0

    return {
        "total": total,
        "covered": covered,
        "percentage": pct,
        "endpoints": details,
    }


def generate_html(coverage: dict) -> str:
    pct = coverage["percentage"]
    total = coverage["total"]
    covered = coverage["covered"]
    bar_color = "#4caf50" if pct >= 50 else ("#ff9800" if pct >= 30 else "#f44336")

    rows = ""
    for ep in coverage["endpoints"]:
        status_class = "covered" if ep["covered"] else "missed"
        badge = "COVERED" if ep["covered"] else "NOT COVERED"
        statuses = ", ".join(str(s) for s in ep["statuses"]) if ep["statuses"] else "&mdash;"
        rows += f"""
        <tr class="{status_class}">
          <td><span class="badge {status_class}">{badge}</span></td>
          <td><code>{ep['method']}</code></td>
          <td><code>{ep['path']}</code></td>
          <td>{ep['summary']}</td>
          <td>{statuses}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Swagger Coverage Report</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         background: #f5f5f5; color: #333; padding: 24px; }}
  .container {{ max-width: 1100px; margin: 0 auto; }}
  h1 {{ margin-bottom: 16px; font-size: 28px; }}
  .summary {{ background: #fff; border-radius: 8px; padding: 24px; margin-bottom: 24px;
              box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  .summary h2 {{ font-size: 20px; margin-bottom: 12px; }}
  .progress-bar {{ width: 100%; height: 28px; background: #e0e0e0; border-radius: 14px;
                   overflow: hidden; margin-bottom: 8px; }}
  .progress-fill {{ height: 100%; background: {bar_color}; border-radius: 14px;
                    display: flex; align-items: center; justify-content: center;
                    color: #fff; font-weight: 600; font-size: 14px;
                    min-width: 60px; transition: width 0.3s; }}
  .stats {{ font-size: 14px; color: #666; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px;
           overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  th {{ background: #fafafa; text-align: left; padding: 12px 16px; font-size: 13px;
       text-transform: uppercase; color: #888; border-bottom: 2px solid #eee; }}
  td {{ padding: 10px 16px; border-bottom: 1px solid #f0f0f0; font-size: 14px; }}
  tr.missed td {{ background: #fff5f5; }}
  tr.covered td {{ background: #f5fff5; }}
  .badge {{ padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
  .badge.covered {{ background: #c8e6c9; color: #2e7d32; }}
  .badge.missed {{ background: #ffcdd2; color: #c62828; }}
  code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 4px; font-size: 13px; }}
</style>
</head>
<body>
<div class="container">
  <h1>Swagger API Coverage Report</h1>
  <div class="summary">
    <h2>Overall Coverage</h2>
    <div class="progress-bar">
      <div class="progress-fill" style="width: {max(pct, 5)}%">{pct}%</div>
    </div>
    <p class="stats">{covered} of {total} endpoints covered</p>
  </div>
  <table>
    <thead>
      <tr><th>Status</th><th>Method</th><th>Path</th><th>Summary</th><th>Response Codes</th></tr>
    </thead>
    <tbody>{rows}
    </tbody>
  </table>
</div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate swagger-coverage report")
    parser.add_argument("--spec-url", default="http://localhost:4111",
                        help="Base URL of the running backend (to download OpenAPI spec)")
    parser.add_argument("--input-dir", default="swagger-coverage-output",
                        help="Directory with logged request JSON files")
    parser.add_argument("--output-dir", default="swagger-coverage-report",
                        help="Output directory for the report")
    args = parser.parse_args()

    spec = fetch_openapi_spec(args.spec_url)
    if spec:
        print(f"Downloaded OpenAPI spec: {len(spec.get('paths', {}))} paths")
        spec_endpoints = extract_spec_endpoints(spec)
    else:
        print("Could not download OpenAPI spec, using fallback endpoint list")
        spec_endpoints = FALLBACK_SPEC_ENDPOINTS

    logged = load_logged_requests(args.input_dir)
    print(f"Loaded {len(logged)} logged API requests")

    coverage = compute_coverage(spec_endpoints, logged)
    print(f"Coverage: {coverage['covered']}/{coverage['total']} = {coverage['percentage']}%")

    os.makedirs(args.output_dir, exist_ok=True)

    with open(os.path.join(args.output_dir, "coverage.json"), "w") as f:
        json.dump(coverage, f, indent=2)

    with open(os.path.join(args.output_dir, "index.html"), "w") as f:
        f.write(generate_html(coverage))

    print(f"Report saved to {args.output_dir}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
