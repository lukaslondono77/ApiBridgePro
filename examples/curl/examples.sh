#!/bin/bash
# ApiBridge Pro - curl Examples
# Demonstrates various features using curl commands

set -e

BASE_URL="http://localhost:8000"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         ApiBridge Pro - curl Examples                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 1. Health Check
echo "1️⃣  Health Check"
echo "   Command: curl $BASE_URL/health"
echo ""
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""
echo "   ✅ System is healthy!"
echo ""

# 2. Weather API (Multi-Provider)
echo "2️⃣  Weather API (Multi-Provider with Failover)"
echo "   Command: curl '$BASE_URL/proxy/weather_unified/weather?q=London'"
echo ""
curl -s -i "$BASE_URL/proxy/weather_unified/weather?q=London" 2>&1 | head -15
echo ""

# 3. Metrics
echo "3️⃣  Prometheus Metrics"
echo "   Command: curl $BASE_URL/metrics"
echo ""
curl -s "$BASE_URL/metrics" | grep "apibridge_requests_total" | head -5
echo "   ... (200+ metrics available)"
echo ""

# 4. Custom Headers
echo "4️⃣  Check Observability Headers"
echo "   ApiBridge adds these headers for debugging:"
echo ""
RESPONSE=$(curl -s -i "$BASE_URL/proxy/weather_unified/weather?q=Tokyo" 2>&1)
echo "$RESPONSE" | grep -i "X-ApiBridge" || echo "   (Headers appear after successful upstream call)"
echo ""

# 5. Rate Limiting
echo "5️⃣  Rate Limiting (send 15 rapid requests)"
echo ""
for i in {1..15}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health")
  if [ "$STATUS" = "429" ]; then
    echo "   Request $i: ⚠️  Rate limited! (HTTP 429)"
    break
  else
    echo "   Request $i: ✅ OK (HTTP $STATUS)"
  fi
  sleep 0.05
done
echo ""

# 6. Caching Demo
echo "6️⃣  Caching Performance"
echo "   First request (cache miss):"
TIME1=$(curl -s -w "%{time_total}" -o /dev/null "$BASE_URL/health")
echo "   Time: ${TIME1}s"
echo ""
echo "   Second request (cache hit for GET requests):"
TIME2=$(curl -s -w "%{time_total}" -o /dev/null "$BASE_URL/health")
echo "   Time: ${TIME2}s"
echo ""

# 7. Admin Dashboard
echo "7️⃣  Admin Dashboard"
echo "   Open in browser: $BASE_URL/admin"
echo "   Or get JSON: curl $BASE_URL/admin/health-json"
echo ""

# 8. API Documentation
echo "8️⃣  Interactive API Documentation"
echo "   Swagger UI: $BASE_URL/docs"
echo "   ReDoc: $BASE_URL/redoc"
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "🎉 Examples Complete!"
echo ""
echo "💡 Try these URLs in your browser:"
echo "   • Dashboard: $BASE_URL/admin"
echo "   • API Docs:  $BASE_URL/docs"
echo "   • Metrics:   $BASE_URL/metrics"
echo "═══════════════════════════════════════════════════════════════"

