// Planche-contact d'une vidéo YouTube, construite dans la page elle-même.
//
// Usage : ouvrir la vidéo officielle dans le navigateur de l'app Claude,
// exécuter ce fichier dans la page (outil JavaScript ou console), puis :
//   __run(0, 4)                                        // 32 vignettes de 0:00 à 2:04, pas de 4 s
//   __run([606, 607, 608], 0, 0, {cols: 2, tw: 659})   // instants choisis, grandes vignettes
//   await __wait()                                     // attend la fin, renvoie le journal
// La planche s'affiche en haut de la page, par-dessus YouTube ; une capture
// d'écran du navigateur l'enregistre, puis elle est rangée dans media-local/
// (ignoré par git). __plancheOff() retire la planche.
//
// Rien n'est téléchargé : les images sont dessinées depuis l'élément <video>
// de la page, le temps de la capture. Les publicités sont attendues ou
// passées avant chaque image ; une image prise pendant une pub est refaite.

window.__noAd = async () => {
  const p = document.querySelector('#movie_player');
  let k = 0;
  while (p?.classList.contains('ad-showing') && k++ < 120) {
    const v = document.querySelector('video'); v.muted = true; if (v.paused) v.play().catch(() => {});
    document.querySelector('.ytp-skip-ad-button, .ytp-ad-skip-button, .ytp-ad-skip-button-modern')?.click();
    await new Promise(r => setTimeout(r, 500));
  }
  return k;
};

window.__planche = async function (times, opts = {}) {
  const cols = opts.cols || 4, tw = opts.tw || 329, th = Math.round(tw * 9 / 16), lab = 14;
  const rows = Math.ceil(times.length / cols);
  let c = document.getElementById('__pl');
  if (!c) { c = document.createElement('canvas'); c.id = '__pl'; document.body.appendChild(c); }
  c.width = cols * tw; c.height = rows * (th + lab);
  Object.assign(c.style, { position: 'fixed', left: '0', top: '0', zIndex: 2147483647, background: '#000', width: c.width + 'px', height: c.height + 'px' });
  const g = c.getContext('2d'); g.fillStyle = '#000'; g.fillRect(0, 0, c.width, c.height);
  const fmt = s => { const m = Math.floor(s / 60), r = s - m * 60; return m + ':' + (Number.isInteger(r) ? String(r).padStart(2, '0') : r.toFixed(1).padStart(4, '0')); };
  const log = [];
  for (let i = 0; i < times.length; i++) {
    const t = times[i];
    for (let attempt = 0; attempt < 3; attempt++) {
      if (await window.__noAd()) log.push('pub@' + t);
      const v = document.querySelector('video'); v.muted = true; v.pause();
      await new Promise(res => { const done = () => { v.removeEventListener('seeked', done); res(); }; v.addEventListener('seeked', done); v.currentTime = t; setTimeout(done, 6000); });
      let k = 0; while (v.readyState < 2 && k++ < 30) await new Promise(r => setTimeout(r, 200));
      await new Promise(r => setTimeout(r, 150));
      if (document.querySelector('#movie_player')?.classList.contains('ad-showing')) continue;
      if (Math.abs(v.currentTime - t) > 1) { log.push('derive ' + t + '->' + v.currentTime.toFixed(1)); continue; }
      const x = (i % cols) * tw, y = Math.floor(i / cols) * (th + lab);
      g.drawImage(v, x, y + lab, tw, th);
      g.fillStyle = '#ff0'; g.font = 'bold 12px monospace'; g.fillText(fmt(t), x + 3, y + 11);
      break;
    }
  }
  return log;
};

window.__run = (start, step, n = 32, opts = { cols: 4, tw: 329 }) => {
  window.__st = { busy: true, start };
  const ts = Array.isArray(start) ? start : Array.from({ length: n }, (_, i) => start + i * step);
  window.__planche(ts, opts).then(log => { window.scrollTo(0, 0); window.__st = { busy: false, from: ts[0], to: ts[ts.length - 1], log }; });
  return 'lancé';
};
window.__wait = async (max = 40000) => { const t0 = Date.now(); while (window.__st?.busy && Date.now() - t0 < max) await new Promise(r => setTimeout(r, 500)); return JSON.stringify(window.__st); };
window.__plancheOff = () => document.getElementById('__pl')?.remove();
