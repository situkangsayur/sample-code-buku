// Dijalankan di worker thread: punya event loop dan memori JS sendiri.
const { parentPort } = require('node:worker_threads');
let x = 0;
for (let i = 0; i < 3e9; i++) x += i;
parentPort.postMessage(x);
