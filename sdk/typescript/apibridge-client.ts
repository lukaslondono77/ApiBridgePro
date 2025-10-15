/**
 * ApiBridge Pro - Official TypeScript/JavaScript Client SDK
 * 
 * Install:
 *   npm install node-fetch
 *   # or use built-in fetch in Node 18+
 * 
 * Usage:
 *   import { ApiBridgeClient } from './apibridge-client';
 *   
 *   const client = new ApiBridgeClient({
 *     baseUrl: 'https://api.example.com',
 *     apiKey: process.env.APIBRIDGE_KEY
 *   });
 *   
 *   // Get weather
 *   const weather = await client.proxy('weather_unified', '/weather', {
 *     params: { q: 'London' }
 *   });
 *   const data = await weather.json();
 */

export interface ApiBridgeConfig {
  baseUrl: string;
  apiKey?: string;
  timeout?: number;
  maxRetries?: number;
}

export interface ProxyOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  params?: Record<string, string | number | boolean>;
  body?: any;
  headers?: Record<string, string>;
}

export interface HealthResponse {
  ok: boolean;
  mode: string;
  connectors: string[];
}

export interface MetricsInfo {
  requests_total: number;
  cache_hits: number;
  budget_spent: number;
  // ... other metrics
}

export class ApiBridgeClient {
  private baseUrl: string;
  private apiKey?: string;
  private timeout: number;
  private maxRetries: number;

  constructor(config: ApiBridgeConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, '');
    this.apiKey = config.apiKey;
    this.timeout = config.timeout || 30000;
    this.maxRetries = config.maxRetries || 3;
  }

  /**
   * Make request through ApiBridge connector.
   * 
   * @param connector - Connector name (e.g., "weather_unified")
   * @param path - API path (e.g., "/weather")
   * @param options - Request options
   * @returns Promise<Response>
   */
  async proxy(
    connector: string,
    path: string,
    options: ProxyOptions = {}
  ): Promise<Response> {
    const url = `${this.baseUrl}/proxy/${connector}/${path.replace(/^\//, '')}`;
    const headers: Record<string, string> = options.headers || {};
    
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    // Build query string
    const params = options.params ? new URLSearchParams(
      Object.entries(options.params).map(([k, v]) => [k, String(v)])
    ) : null;
    const queryString = params?.toString() ? `?${params}` : '';

    // Retry logic
    let lastError: Error | null = null;
    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

        const response = await fetch(`${url}${queryString}`, {
          method: options.method || 'GET',
          headers: {
            'Content-Type': 'application/json',
            ...headers
          },
          body: options.body ? JSON.stringify(options.body) : undefined,
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        // Don't retry on 4xx errors
        if (response.status >= 400 && response.status < 500) {
          return response;
        }

        // Retry on 5xx
        if (response.status >= 500 && attempt < this.maxRetries - 1) {
          await this.sleep(Math.pow(2, attempt) * 1000); // Exponential backoff
          continue;
        }

        return response;

      } catch (error) {
        lastError = error as Error;
        if (attempt < this.maxRetries - 1) {
          await this.sleep(Math.pow(2, attempt) * 1000);
          continue;
        }
      }
    }

    throw lastError || new Error('All retries failed');
  }

  /**
   * Check ApiBridge health.
   */
  async health(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }

  /**
   * Get Prometheus metrics.
   */
  async metrics(): Promise<string> {
    const response = await fetch(`${this.baseUrl}/metrics`);
    return response.text();
  }

  /**
   * Get admin dashboard data.
   */
  async adminStats(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/admin/health-json`);
    return response.json();
  }

  /**
   * Typed connector access (experimental).
   * 
   * Example:
   *   client.connector('weather_unified').get('/weather', { q: 'London' })
   */
  connector(name: string) {
    return {
      get: (path: string, params?: Record<string, any>) =>
        this.proxy(name, path, { method: 'GET', params }),
      
      post: (path: string, body?: any, params?: Record<string, any>) =>
        this.proxy(name, path, { method: 'POST', body, params }),
      
      put: (path: string, body?: any, params?: Record<string, any>) =>
        this.proxy(name, path, { method: 'PUT', body, params }),
      
      delete: (path: string, params?: Record<string, any>) =>
        this.proxy(name, path, { method: 'DELETE', params }),
    };
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Example usage
async function example() {
  const client = new ApiBridgeClient({
    baseUrl: 'http://localhost:8000',
    timeout: 10000
  });

  try {
    // Check health
    const health = await client.health();
    console.log('System healthy:', health.ok);
    console.log('Available connectors:', health.connectors);

    // Use typed connector access
    const weather = await client.connector('weather_unified').get('/weather', { q: 'London' });
    const data = await weather.json();
    console.log('Weather:', data);

  } catch (error) {
    console.error('Error:', error);
  }
}

// Run example if executed directly
if (require.main === module) {
  example();
}

export { ApiBridgeClient };
export type { ApiBridgeConfig, ProxyOptions, HealthResponse };

