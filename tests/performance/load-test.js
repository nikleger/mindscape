import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Ramp up to 20 users
    { duration: '1m', target: 20 }, // Stay at 20 users for 1 minute
    { duration: '30s', target: 0 }, // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.01'], // Less than 1% of requests should fail
  },
};

const BASE_URL = 'http://localhost:3000';

export default function () {
  // Test homepage load
  let res = http.get(`${BASE_URL}/`);
  check(res, {
    'homepage status is 200': (r) => r.status === 200,
    'homepage loads within 500ms': (r) => r.timings.duration < 500,
  });

  // Test mindmap creation
  res = http.post(`${BASE_URL}/api/mindmaps`, JSON.stringify({
    title: 'Performance Test Mindmap',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });
  check(res, {
    'mindmap creation status is 201': (r) => r.status === 201,
  });

  const mindmapId = JSON.parse(res.body).id;

  // Test node creation
  res = http.post(`${BASE_URL}/api/mindmaps/${mindmapId}/nodes`, JSON.stringify({
    content: 'Test Node',
    x: 100,
    y: 100,
  }), {
    headers: { 'Content-Type': 'application/json' },
  });
  check(res, {
    'node creation status is 201': (r) => r.status === 201,
  });

  // Test mindmap retrieval
  res = http.get(`${BASE_URL}/api/mindmaps/${mindmapId}`);
  check(res, {
    'mindmap retrieval status is 200': (r) => r.status === 200,
    'mindmap contains created node': (r) => JSON.parse(r.body).nodes.length > 0,
  });

  sleep(1);
} 