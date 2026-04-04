const fs = require('fs');

function createIconSVG(size) {
  const r = size * 0.45;
  const cx = size / 2;
  const cy = size / 2;
  const fontSize = size * 0.5;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea"/>
      <stop offset="100%" style="stop-color:#764ba2"/>
    </linearGradient>
  </defs>
  <circle cx="${cx}" cy="${cy}" r="${r}" fill="url(#bg)"/>
  <text x="${cx}" y="${cy}" text-anchor="middle" dominant-baseline="central"
    font-family="Arial,sans-serif" font-size="${fontSize}" font-weight="bold" fill="white">T</text>
</svg>`;
}

// Save as SVG (browsers accept SVG icons too, but we need PNG for PWA)
// We'll create a simple canvas-based PNG using a data URL approach
// Actually, let's create proper PNGs with a minimal approach

const { createCanvas } = (() => {
  try { return require('canvas'); } catch(e) { return { createCanvas: null }; }
})();

if (createCanvas) {
  [192, 512].forEach(size => {
    const canvas = createCanvas(size, size);
    const ctx = canvas.getContext('2d');
    // Gradient background circle
    const cx = size/2, cy = size/2, r = size*0.45;
    const grad = ctx.createLinearGradient(0, 0, size, size);
    grad.addColorStop(0, '#667eea');
    grad.addColorStop(1, '#764ba2');
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI*2);
    ctx.fillStyle = grad;
    ctx.fill();
    // Letter T
    ctx.fillStyle = 'white';
    ctx.font = `bold ${size*0.5}px Arial`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('T', cx, cy);
    fs.writeFileSync(`icon-${size}.png`, canvas.toBuffer('image/png'));
    console.log(`icon-${size}.png created`);
  });
} else {
  // Fallback: create SVG icons and a simple 1x1 PNG placeholder
  // For PWA we need PNG, so let's create minimal valid PNGs programmatically

  function createMinimalPNG(size) {
    // Create an uncompressed PNG with the gradient circle and T letter
    // Using raw PNG creation (minimal, no dependencies)

    const { deflateSync } = require('zlib');
    const width = size, height = size;
    const cx = width/2, cy = height/2, r = width*0.45;

    // Create pixel data (RGBA)
    const pixels = Buffer.alloc(width * height * 4, 0);

    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const idx = (y * width + x) * 4;
        const dx = x - cx, dy = y - cy;
        const dist = Math.sqrt(dx*dx + dy*dy);

        if (dist <= r) {
          // Inside circle - gradient from #667eea to #764ba2
          const t = (x + y) / (width + height);
          const r1 = 0x66 + (0x76-0x66)*t, g1 = 0x7e + (0x4b-0x7e)*t, b1 = 0xea + (0xa2-0xea)*t;

          // Check if this pixel is part of the "T" letter
          const relX = (x - cx) / (r * 0.8);
          const relY = (y - cy) / (r * 0.8);

          const isT = (
            (relY >= -0.55 && relY <= -0.25 && relX >= -0.4 && relX <= 0.4) || // top bar
            (relX >= -0.12 && relX <= 0.12 && relY >= -0.55 && relY <= 0.55)    // vertical bar
          );

          if (isT) {
            pixels[idx] = 255;
            pixels[idx+1] = 255;
            pixels[idx+2] = 255;
            pixels[idx+3] = 255;
          } else {
            pixels[idx] = Math.round(r1);
            pixels[idx+1] = Math.round(g1);
            pixels[idx+2] = Math.round(b1);
            pixels[idx+3] = 255;
          }
        }
        // else transparent (already 0)
      }
    }

    // Build PNG file
    const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

    function chunk(type, data) {
      const len = Buffer.alloc(4);
      len.writeUInt32BE(data.length);
      const typeB = Buffer.from(type);
      const crcData = Buffer.concat([typeB, data]);
      let crc = crc32(crcData);
      const crcB = Buffer.alloc(4);
      crcB.writeUInt32BE(crc >>> 0);
      return Buffer.concat([len, typeB, data, crcB]);
    }

    function crc32(buf) {
      let c = 0xffffffff;
      for (let i = 0; i < buf.length; i++) {
        c ^= buf[i];
        for (let j = 0; j < 8; j++) {
          c = (c >>> 1) ^ (c & 1 ? 0xedb88320 : 0);
        }
      }
      return c ^ 0xffffffff;
    }

    // IHDR
    const ihdr = Buffer.alloc(13);
    ihdr.writeUInt32BE(width, 0);
    ihdr.writeUInt32BE(height, 4);
    ihdr[8] = 8; // bit depth
    ihdr[9] = 6; // RGBA
    ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;

    // IDAT - add filter byte (0) before each row
    const rawData = Buffer.alloc(height * (1 + width * 4));
    for (let y = 0; y < height; y++) {
      rawData[y * (1 + width * 4)] = 0; // filter none
      pixels.copy(rawData, y * (1 + width * 4) + 1, y * width * 4, (y + 1) * width * 4);
    }
    const compressed = deflateSync(rawData);

    // IEND
    const iend = Buffer.alloc(0);

    const png = Buffer.concat([
      signature,
      chunk('IHDR', ihdr),
      chunk('IDAT', compressed),
      chunk('IEND', iend),
    ]);

    return png;
  }

  [192, 512].forEach(size => {
    const png = createMinimalPNG(size);
    fs.writeFileSync(`icon-${size}.png`, png);
    console.log(`icon-${size}.png created (${(png.length/1024).toFixed(1)} KB)`);
  });
}
