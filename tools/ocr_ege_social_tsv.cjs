const fs = require('node:fs');
const path = require('node:path');
const { createWorker } = require('tesseract.js');

(async () => {
  const root = 'review/ege-social-2027-fipi';
  const output = path.join(root, 'tsv');
  fs.mkdirSync(output, { recursive: true });
  const queue = fs.readdirSync(path.join(root, 'pages'))
    .filter((name) => /^page-(?:0(?:0[9]|[1-9]\d)|1\d\d|2(?:[0-6]\d|7[01]))\.png$/.test(name))
    .filter((name) => !fs.existsSync(path.join(output, name.replace('.png', '.tsv'))))
    .sort();

  await Promise.all(Array.from({ length: 8 }, async () => {
    const worker = await createWorker('rus');
    try {
      while (queue.length) {
        const name = queue.shift();
        const result = await worker.recognize(path.join(root, 'pages', name), {}, { text: false, tsv: true });
        fs.writeFileSync(path.join(output, name.replace('.png', '.tsv')), result.data.tsv);
        console.log(name);
      }
    } finally {
      await worker.terminate();
    }
  }));
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
