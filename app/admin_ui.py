"""
Admin UI - Dashboard for budgets, health, and cache statistics
"""
import time
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/admin", tags=["admin"])

def _get_dashboard_html(stats: dict[str, Any]) -> str:
    """Generate admin dashboard HTML"""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ApiBridge Pro - Admin Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            line-height: 1.6;
            padding: 2rem;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .subtitle {{
            color: #94a3b8;
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .card {{
            background: #1e293b;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #334155;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        .card h2 {{
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: #f1f5f9;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .card h2::before {{
            content: '';
            display: inline-block;
            width: 4px;
            height: 1.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
        }}
        .stat {{
            display: flex;
            justify-content: space-between;
            padding: 0.75rem 0;
            border-bottom: 1px solid #334155;
        }}
        .stat:last-child {{
            border-bottom: none;
        }}
        .stat-label {{
            color: #94a3b8;
            font-weight: 500;
        }}
        .stat-value {{
            color: #f1f5f9;
            font-weight: 600;
        }}
        .health-indicator {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 0.5rem;
        }}
        .health-healthy {{
            background: #10b981;
            box-shadow: 0 0 8px #10b981;
        }}
        .health-unhealthy {{
            background: #ef4444;
            box-shadow: 0 0 8px #ef4444;
        }}
        .budget-bar {{
            width: 100%;
            height: 8px;
            background: #334155;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
        }}
        .budget-fill {{
            height: 100%;
            background: linear-gradient(90deg, #10b981 0%, #f59e0b 70%, #ef4444 100%);
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
        .refresh-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 6px rgba(102, 126, 234, 0.4);
        }}
        .refresh-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(102, 126, 234, 0.5);
        }}
        .refresh-btn:active {{
            transform: translateY(0);
        }}
        .timestamp {{
            color: #64748b;
            font-size: 0.875rem;
            margin-top: 2rem;
            text-align: center;
        }}
        .tag {{
            display: inline-block;
            background: #334155;
            color: #e2e8f0;
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            font-size: 0.875rem;
            font-weight: 500;
        }}
        .tag-success {{
            background: #10b98133;
            color: #10b981;
        }}
        .tag-warning {{
            background: #f59e0b33;
            color: #f59e0b;
        }}
        .tag-danger {{
            background: #ef444433;
            color: #ef4444;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            text-align: left;
            padding: 0.75rem;
            background: #0f172a;
            color: #94a3b8;
            font-weight: 600;
            border-bottom: 2px solid #334155;
        }}
        td {{
            padding: 0.75rem;
            border-bottom: 1px solid #334155;
        }}
        tr:hover {{
            background: #0f172a;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 ApiBridge Pro</h1>
        <p class="subtitle">Admin Dashboard - Monitor your API gateway in real-time</p>

        <div style="margin-bottom: 2rem;">
            <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Dashboard</button>
        </div>

        <div class="grid">
            <!-- System Overview -->
            <div class="card">
                <h2>System Overview</h2>
                <div class="stat">
                    <span class="stat-label">Mode</span>
                    <span class="stat-value"><span class="tag tag-success">{stats.get('mode', 'live').upper()}</span></span>
                </div>
                <div class="stat">
                    <span class="stat-label">Connectors</span>
                    <span class="stat-value">{stats.get('total_connectors', 0)}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Active Providers</span>
                    <span class="stat-value">{stats.get('total_providers', 0)}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Cache Entries</span>
                    <span class="stat-value">{stats.get('cache_entries', 0)}</span>
                </div>
            </div>

            <!-- Budget Overview -->
            <div class="card">
                <h2>Budget Overview</h2>
                {_render_budgets(stats.get('budgets', {}))}
            </div>

            <!-- Rate Limiting -->
            <div class="card">
                <h2>Rate Limiting</h2>
                {_render_rate_limits(stats.get('rate_limits', {}))}
            </div>
        </div>

        <!-- Provider Health -->
        <div class="card" style="margin-bottom: 2rem;">
            <h2>Provider Health</h2>
            <table>
                <thead>
                    <tr>
                        <th>Connector</th>
                        <th>Provider</th>
                        <th>Status</th>
                        <th>Avg Latency</th>
                        <th>Last Check</th>
                    </tr>
                </thead>
                <tbody>
                    {_render_provider_health(stats.get('provider_health', {}))}
                </tbody>
            </table>
        </div>

        <!-- Cache Statistics -->
        <div class="card">
            <h2>Cache Statistics</h2>
            <table>
                <thead>
                    <tr>
                        <th>Key</th>
                        <th>Expires At</th>
                        <th>Size</th>
                    </tr>
                </thead>
                <tbody>
                    {_render_cache_stats(stats.get('cache_stats', {}))}
                </tbody>
            </table>
        </div>

        <p class="timestamp">Last updated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}</p>
    </div>

    <script>
        // Auto-refresh every 10 seconds
        setTimeout(() => location.reload(), 10000);
    </script>
</body>
</html>
"""

def _render_budgets(budgets: dict) -> str:
    if not budgets:
        return '<div class="stat"><span class="stat-label">No budget data</span></div>'

    html = ""
    for connector, data in budgets.items():
        spent = data.get('spent', 0)
        limit = data.get('limit', 100)
        percentage = min(100, (spent / limit * 100)) if limit > 0 else 0
        tag_class = "tag-success" if percentage < 70 else ("tag-warning" if percentage < 90 else "tag-danger")

        html += f'''
        <div class="stat">
            <span class="stat-label">{connector}</span>
            <span class="stat-value">${spent:.2f} / ${limit:.2f}</span>
        </div>
        <div class="budget-bar">
            <div class="budget-fill" style="width: {percentage}%"></div>
        </div>
        '''
    return html

def _render_rate_limits(limits: dict) -> str:
    if not limits:
        return '<div class="stat"><span class="stat-label">No rate limit data</span></div>'

    html = ""
    for name, data in limits.items():
        html += f'''
        <div class="stat">
            <span class="stat-label">{name}</span>
            <span class="stat-value">{data.get('tokens', 0):.1f} / {data.get('capacity', 10)} tokens</span>
        </div>
        '''
    return html

def _render_provider_health(health: dict) -> str:
    if not health:
        return '<tr><td colspan="5" style="text-align: center; color: #64748b;">No provider health data</td></tr>'

    html = ""
    for pkey, data in health.items():
        connector, provider = pkey.split(':', 1) if ':' in pkey else (pkey, 'default')
        healthy = data.get('healthy', False)
        avg_latency = data.get('avg', 0)
        last_check = data.get('ts', 0)

        status_class = "health-healthy" if healthy else "health-unhealthy"
        status_text = "Healthy" if healthy else "Unhealthy"
        time_ago = f"{int(time.time() - last_check)}s ago" if last_check > 0 else "Never"

        html += f'''
        <tr>
            <td>{connector}</td>
            <td>{provider}</td>
            <td><span class="health-indicator {status_class}"></span>{status_text}</td>
            <td>{avg_latency}ms</td>
            <td>{time_ago}</td>
        </tr>
        '''
    return html

def _render_cache_stats(cache: dict) -> str:
    if not cache:
        return '<tr><td colspan="3" style="text-align: center; color: #64748b;">Cache is empty</td></tr>'

    html = ""
    for key, data in cache.items():
        expires = data.get('expires', 0)
        size = data.get('size', 0)
        expires_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expires)) if expires > 0 else 'N/A'

        html += f'''
        <tr>
            <td style="font-family: monospace; font-size: 0.875rem;">{key[:60]}...</td>
            <td>{expires_str}</td>
            <td>{size} bytes</td>
        </tr>
        '''
    return html[:5000]  # Limit HTML size

@router.get("", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Render admin dashboard"""
    from .caching import _cache
    from .config import CONNECTORS_FILE, MODE, load_config
    from .connectors import build_connector_policies
    from .health import _health
    from .rate_limit import _buckets

    # Gather statistics
    config = load_config(CONNECTORS_FILE)
    policies = build_connector_policies(config)

    stats = {
        'mode': MODE,
        'total_connectors': len(policies),
        'total_providers': sum(len(p.providers) if p.providers else 1 for p in policies.values()),
        'cache_entries': len(_cache),
        'provider_health': _health,
        'budgets': {},
        'rate_limits': {},
        'cache_stats': {}
    }

    # Budget stats (would need to fetch from budget guard)
    for name, policy in policies.items():
        if policy.budget and policy.budget.get('monthly_usd_max'):
            stats['budgets'][name] = {
                'spent': 0,  # Would fetch from budget guard
                'limit': float(policy.budget['monthly_usd_max'])
            }

    # Rate limit stats
    for name, bucket in _buckets.items():
        stats['rate_limits'][name] = {
            'tokens': bucket.tokens,
            'capacity': bucket.capacity
        }

    # Cache stats
    for key, (exp, content, headers, status) in _cache.items():
        if len(stats['cache_stats']) < 50:  # Limit to 50 entries
            stats['cache_stats'][key] = {
                'expires': exp,
                'size': len(content)
            }

    return _get_dashboard_html(stats)

@router.get("/health-json")
async def health_json():
    """Get health data as JSON"""
    from .health import _health
    return {"provider_health": _health}

@router.get("/cache-json")
async def cache_json():
    """Get cache statistics as JSON"""
    from .caching import _cache
    stats = {}
    for key, (exp, content, headers, status) in _cache.items():
        stats[key] = {
            'expires_at': exp,
            'size': len(content),
            'status': status
        }
    return stats


