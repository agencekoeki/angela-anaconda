// Planche contact d'une vidéo YouTube, dessinée dans la page elle-même.
//
// Usage, dans l'onglet de la vidéo officielle (Claude in Chrome, outil JavaScript) :
//   1. coller ce fichier entier dans javascript_tool ;
//   2. __run(30, 5)          // 30 vignettes à partir de 0:30, une toutes les 5 s
//      await __wait(44000)   // attend la fin (relancer __wait si busy:true)
//   3. capture d'écran avec save_to_disk:true : c'est la planche ;
//   4. __plancheOff() pour la retirer.
//   __run([606, 607, 608], 0, 0, {cols: 3})  // instants choisis, grandes vignettes
//
// La planche occupe toute la fenêtre (6 colonnes × 5 rangées par défaut), pour que
// la capture soit lisible : c'est la taille de la fenêtre qui fixe celle des vignettes.
// Rien n'est téléchargé : les images sont dessinées depuis l'élément <video> le temps
// de la capture. Les pubs sont attendues ou passées ; une image prise pendant une pub
// est refaite. Les planches restent dans media-local/, jamais dans un dépôt.

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
  const cols = opts.cols || 6;
  const tw = opts.tw || Math.floor(innerWidth / cols);
  const th = Math.round(tw * 9 / 16), lab = 14;
  const rows = Math.ceil(times.length / cols);
  let c = document.getElementById('__pl');
  if (!c) { c = document.createElement('canvas'); c.id = '__pl'; document.body.appendChild(c); }
  c.width = cols * tw; c.height = rows * (th + lab);
  Object.assign(c.style, { position: 'fixed', left: '0', top: '0', zIndex: 2147483647, background: '#000', width: c.width + 'px', height: c.height + 'px' });
  const g = c.getContext('2d'); g.fillStyle = '#000'; g.fillRect(0, 0, c.width, c.height);
  const fmt = s => { const m = Math.floor(s / 60), r = Math.round(s - m * 60); return m + ':' + String(r).padStart(2, '0'); };
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

// L'outil JavaScript coupe au bout d'environ 45 s : __run lance en tâche de fond,
// __wait sonde. Une planche de 30 images prend de 40 à 70 s.
window.__run = (start, step, n = 30, opts = {}) => {
  window.__st = { busy: true, start };
  const ts = Array.isArray(start) ? start : Array.from({ length: n }, (_, i) => start + i * step);
  window.__planche(ts, opts).then(log => { window.scrollTo(0, 0); window.__st = { busy: false, from: ts[0], to: ts[ts.length - 1], log }; });
  return 'lancé';
};
window.__wait = async (max = 40000) => { const t0 = Date.now(); while (window.__st?.busy && Date.now() - t0 < max) await new Promise(r => setTimeout(r, 500)); return JSON.stringify(window.__st); };
window.__plancheOff = () => document.getElementById('__pl')?.remove();
