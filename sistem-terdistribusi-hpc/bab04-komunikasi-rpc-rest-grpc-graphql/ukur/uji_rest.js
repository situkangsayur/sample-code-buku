// Uji beban REST dengan k6 (https://k6.io). k6 adalah program tersendiri,
// bukan paket npm; skrip ini dijalankan oleh k6, bukan oleh Node.js.
//
//   k6 run ukur/uji_rest.js
//   k6 run -e URL=http://localhost:18080 -e VUS=200 ukur/uji_rest.js
//
// Padanannya untuk gRPC dengan ghz (lihat ukur/uji_grpc.sh):
// ghz --insecure --proto katalog.proto --call katalog.v1.Katalog.AmbilProduk \
//     -d '{"id": 42}' -m '{"authorization":"Bearer rahasia"}' -c 50 -n 20000 localhost:50051
import http from 'k6/http';
import { check } from 'k6';

const URL = __ENV.URL || 'http://localhost:8080';

export const options = {
  vus: Number(__ENV.VUS || 50), duration: __ENV.DURASI || '30s',
  summaryTrendStats: ['avg', 'p(50)', 'p(99)', 'max'],
};

export default function () {
  const r = http.get(`${URL}/v1/produk/42`);
  check(r, { 'status 200': (x) => x.status === 200 });
}
