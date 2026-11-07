// Kode 6.12: Node.js unggul untuk I/O, tetapi rapuh untuk CPU.
// Jalankan: npm install && npm start   (port lain: PORT=3999 npm start)
// Uji di terminal lain:
//   curl localhost:3000/saldo?id=1            (cepat)
//   curl localhost:3000/laporan-lambat &      (membekukan server beberapa detik)
//   curl localhost:3000/saldo?id=1            (ikut menunggu!)
//   curl localhost:3000/laporan               (kerja CPU di worker thread, server tetap responsif)
const express = require('express');
const { Worker } = require('node:worker_threads');
const path = require('node:path');
const app = express();

// pengganti basis data: kueri 20 ms yang tidak memblokir event loop
const db = {
  query: (sql, params) =>
    new Promise(ok => setTimeout(() => ok({ rows: [{ id: params[0], saldo: 250000 }] }), 20)),
};

// pemantau sederhana: event loop lag (ms) dicetak tiap detik
let terakhir = Date.now();
setInterval(() => {
  const lag = Date.now() - terakhir - 1000;
  if (lag > 50) console.log(`event loop lag: ${lag} ms`);
  terakhir = Date.now();
}, 1000);

// I/O-bound: ribuan permintaan menunggu basis data, tetap satu thread JS
app.get('/saldo', async (req, res) => {
  const s = await db.query('SELECT saldo FROM rekening WHERE id = $1', [req.query.id]);
  res.json(s.rows[0]);
});

// CPU-bound: loop ini membekukan SEMUA permintaan lain selama berjalan
app.get('/laporan-lambat', (req, res) => {
  let x = 0;
  for (let i = 0; i < 3e9; i++) x += i;
  res.json({ x });
});

// perbaikan: pindahkan kerja CPU ke worker thread
app.get('/laporan', (req, res) => {
  const w = new Worker(path.join(__dirname, 'hitung-laporan.js'));
  w.once('message', x => res.json({ x }));
  w.once('error', e => res.status(500).json({ galat: String(e) }));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`siap di http://localhost:${PORT}`));
