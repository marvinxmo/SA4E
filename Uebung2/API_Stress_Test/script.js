import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export let errorRate = new Rate('errors');

export let options = {
    stages: [
        // { duration: '10s', target: 15000 }, // ramp-up to 10 users
        // { duration: '1m', target: 15000 },  // st
        // ay at 10 users
        // { duration: '10s', target: 0 },  // ramp-down to 0 users
        { duration: '1s', target: 15800 },  // ramp-down to 0 users
    ],
    thresholds: {
        errors: ['rate<0.01'], // <1% errors
    },
};

const BASE_URL = 'http://localhost:8086';

export default function () {

    let payload = JSON.stringify({
        name: 'John',
        wish: 'PS5',
        status: 1,
    });

    let params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    let res = http.post(`${BASE_URL}/api/wish`, payload, params);
    check(res, {
        'status is 200': (r) => r.status === 200,
    }) || errorRate.add(1);

    sleep(1);
}