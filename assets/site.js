// HUD 版式脚本：时钟 + GitHub 实时数据 + 复制提示
(function () {
  function pad(n) { return String(n).padStart(2, '0'); }
  var clock = document.getElementById('hudClock');
  if (clock) {
    setInterval(function () {
      var d = new Date();
      clock.textContent = pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
    }, 1000);
  }

  document.addEventListener('click', function (event) {
    var button = event.target.closest ? event.target.closest('[data-copy-value]') : null;
    if (!button) { return; }
    var value = button.getAttribute('data-copy-value');
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(value).then(function () {
        var old = button.textContent;
        button.textContent = '已复制';
        setTimeout(function () { button.textContent = old; }, 1500);
      });
    }
  });

  var data = window.SITE_CONTENT || {};
  var cfg = data.github || {};
  var live = document.querySelectorAll('[data-live]');
  if (!live.length || !cfg.username) { return; }
  var headers = { 'Accept': 'application/vnd.github+json' };
  if (cfg.token) { headers.Authorization = 'Bearer ' + cfg.token; }

  function set(key, value) {
    document.querySelectorAll('[data-live="' + key + '"]').forEach(function (node) { node.textContent = value; });
  }
  function fmt(n) { return n >= 1000 ? (n / 1000).toFixed(1).replace(/\.0$/, '') + 'k' : String(n); }

  fetch('https://api.github.com/users/' + encodeURIComponent(cfg.username), { headers: headers })
    .then(function (r) { return r.json(); })
    .then(function (u) {
      if (!u || u.errored) { return; }
      set('followers', u.followers);
      set('publicRepos', u.public_repos);
    })
    .catch(function () {});

  fetch('https://api.github.com/search/issues?q=' + encodeURIComponent('is:pr author:' + cfg.username + ' is:merged') + '&per_page=1', { headers: headers })
    .then(function (r) { return r.json(); })
    .then(function (res) { if (res && typeof res.total_count === 'number') { set('mergedPRs', res.total_count); } })
    .catch(function () {});

  fetch('https://api.github.com/users/' + encodeURIComponent(cfg.username) + '/repos?per_page=100&sort=stars', { headers: headers })
    .then(function (r) { return r.json(); })
    .then(function (repos) {
      if (!Array.isArray(repos)) { return; }
      var total = 0, top = 0;
      repos.forEach(function (repo) {
        total += repo.stargazers_count || 0;
        if ((repo.stargazers_count || 0) > top) { top = repo.stargazers_count || 0; }
      });
      set('totalStars', fmt(total));
      set('topRepoStars', fmt(top));
    })
    .catch(function () {});
})();
/* ---------- 启动序列（每个会话只播一次） ---------- */
(function () {
  var overlay = document.getElementById('bootOverlay');
  if (!overlay) { return; }
  /* 进站播放一次：站内切页不重播；超过 TTL（默认 30 分钟）重新进站再播 */
  var isEntry = document.body.getAttribute('data-entry') === '1';
  if (!isEntry) {
    overlay.remove();
    document.documentElement.classList.add('no-boot');
    return;
  }
  var TTL = 30 * 60 * 1000;
  var last = 0;
  try { last = Number(sessionStorage.getItem('hud_booted') || 0); } catch (e) { last = 0; }
  var fresh = !last || (Date.now() - last) > TTL;
  var forced = window.location.hash === '#reboot';
  if (!fresh && !forced) {
    overlay.remove();
    document.documentElement.classList.add('no-boot');
    return;
  }
  try { sessionStorage.setItem('hud_booted', String(Date.now())); } catch (e) { /* ignore */ }
  if (forced) { try { sessionStorage.removeItem('hud_booted'); } catch (e) { /* ignore */ } }

  var lines = (window.SITE_CONTENT && window.SITE_CONTENT.boot_lines) || [
    '> loading operator profile ... ok',
    '> all subsystems nominal. welcome, operator.'
  ];
  var log = document.getElementById('bootLog');
  var bar = document.getElementById('bootProgress');
  var index = 0;
  var timer = setInterval(function () {
    if (log) { log.innerHTML = lines[Math.min(index, lines.length - 1)]; }
    if (bar) { bar.style.width = Math.min((index + 1) * (100 / lines.length), 100) + '%'; }
    index += 1;
    if (index > lines.length) {
      clearInterval(timer);
      overlay.classList.add('done');
      setTimeout(function () { if (overlay.parentNode) { overlay.parentNode.removeChild(overlay); } }, 600);
    }
  }, 320);
})();

/* 点品牌可重播启动序列 */
(function () {
  var brand = document.querySelector('.brand-title');
  if (!brand) { return; }
  brand.style.cursor = 'pointer';
  brand.title = '点击重播启动序列';
  brand.addEventListener('click', function () {
    try { sessionStorage.removeItem('hud_booted'); } catch (e) { /* ignore */ }
    window.location.href = window.location.pathname + '#reboot';
    window.location.reload();
  });
})();

/* ---------- 音频引擎（WebAudio 合成，无音频文件） ---------- */
var HudAudio = {
  ctx: null,
  enabled: true,
  started: false,
  master: null,
  init: function () {
    if (this.ctx) { return true; }
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) { this.enabled = false; return false; }
    try { this.ctx = new AC(); } catch (e) { this.enabled = false; return false; }
    this.master = this.ctx.createGain();
    this.master.gain.value = 0.16;
    this.master.connect(this.ctx.destination);
    return true;
  },
  resume: function () {
    if (this.ctx && this.ctx.state === 'suspended') { this.ctx.resume(); }
  },
  /* 低频环境垫：两个失谐三角波 + 低通 */
  ambient: function () {
    if (this.started || !this.ctx) { return; }
    this.started = true;
    var ctx = this.ctx;
    var filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 420;
    filter.Q.value = 0.8;
    var pad = ctx.createGain();
    pad.gain.value = 0.16;
    filter.connect(pad);
    pad.connect(this.master);
    [55, 82.5, 110.3].forEach(function (freq, i) {
      var osc = ctx.createOscillator();
      osc.type = i === 2 ? 'sine' : 'triangle';
      osc.frequency.value = freq;
      var gain = ctx.createGain();
      gain.gain.value = i === 2 ? 0.05 : 0.09;
      osc.connect(gain);
      gain.connect(filter);
      osc.start();
    });
    /* 缓慢起伏 */
    var lfo = ctx.createOscillator();
    var lfoGain = ctx.createGain();
    lfo.frequency.value = 0.08;
    lfoGain.gain.value = 0.06;
    lfo.connect(lfoGain);
    lfoGain.connect(pad.gain);
    lfo.start();
  },
  /* 短促音效 */
  blip: function (freq, duration, type, peak) {
    if (!this.enabled || !this.ctx) { return; }
    this.resume();
    var ctx = this.ctx;
    var osc = ctx.createOscillator();
    var gain = ctx.createGain();
    osc.type = type || 'square';
    osc.frequency.value = freq || 880;
    gain.gain.setValueAtTime(0.0001, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(peak || 0.08, ctx.currentTime + 0.008);
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + (duration || 0.08));
    osc.connect(gain);
    gain.connect(this.master);
    osc.start();
    osc.stop(ctx.currentTime + (duration || 0.08) + 0.02);
  },
  select: function () { this.blip(1180, 0.06, 'square', 0.05); },
  hover: function () { this.blip(1760, 0.03, 'sine', 0.02); },
  toggle: function () { this.blip(660, 0.1, 'triangle', 0.07); }
};

(function () {
  var icon = document.getElementById('soundIcon');
  var status = document.getElementById('soundStatusText');
  var button = document.getElementById('soundToggleBtn');
  function paint() {
    if (icon) { icon.textContent = HudAudio.enabled ? '🔊' : '🔇'; }
    if (status) { status.textContent = HudAudio.enabled ? 'ON' : 'OFF'; }
  }
  paint();
  if (button) {
    button.addEventListener('click', function () {
      HudAudio.enabled = !HudAudio.enabled;
      if (HudAudio.enabled) {
        if (HudAudio.init()) { HudAudio.resume(); HudAudio.ambient(); }
      }
      paint();
      if (HudAudio.enabled) { HudAudio.toggle(); }
    });
  }
  /* 首次交互后启动音频（浏览器自动播放策略） */
  function kick() {
    if (HudAudio.enabled && HudAudio.init()) { HudAudio.resume(); HudAudio.ambient(); }
    document.removeEventListener('pointerdown', kick);
    document.removeEventListener('keydown', kick);
  }
  document.addEventListener('pointerdown', kick);
  document.addEventListener('keydown', kick);

  document.querySelectorAll('.nav-btn, .btn-tactical, .btn-ghost, .contact-line, .lang-btn, .m-nav-btn').forEach(function (el) {
    el.addEventListener('mouseenter', function () { HudAudio.hover(); });
    el.addEventListener('click', function () { HudAudio.select(); });
  });
})();

/* ---------- 神经网络背景 ---------- */
(function () {
  var canvas = document.getElementById('neuralCanvas');
  if (!canvas) { return; }
  var ctx = canvas.getContext('2d');
  var nodes = [];
  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var count = Math.min(70, Math.round(window.innerWidth / 26));
    nodes = [];
    for (var i = 0; i < count; i += 1) {
      nodes.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.28,
        vy: (Math.random() - 0.5) * 0.28,
        r: Math.random() * 1.6 + 0.6
      });
    }
  }
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (var i = 0; i < nodes.length; i += 1) {
      var a = nodes[i];
      a.x += a.vx; a.y += a.vy;
      if (a.x < 0 || a.x > canvas.width) { a.vx *= -1; }
      if (a.y < 0 || a.y > canvas.height) { a.vy *= -1; }
      ctx.beginPath();
      ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0, 240, 255, .32)';
      ctx.fill();
      for (var j = i + 1; j < nodes.length; j += 1) {
        var b = nodes[j];
        var dx = a.x - b.x, dy = a.y - b.y;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 140) {
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = 'rgba(0, 240, 255, ' + (0.13 * (1 - dist / 140)) + ')';
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  resize();
  window.addEventListener('resize', resize);
  draw();
})();

/* ---------- 雷达扫描（带刻度、目标光点与辉光） ---------- */
(function () {
  var canvas = document.getElementById('radarCanvas');
  if (!canvas) { return; }
  var ctx = canvas.getContext('2d');
  var azimuth = document.getElementById('radarAzimuth');
  var angle = 0;
  /* 固定目标点（相对坐标），被扫到时点亮 */
  var targets = [
    { a: 0.6, r: 0.72, label: 'AGENT' },
    { a: 1.9, r: 0.45, label: 'RAG' },
    { a: 3.1, r: 0.83, label: 'EVAL' },
    { a: 4.4, r: 0.33, label: 'OPS' },
    { a: 5.3, r: 0.62, label: 'SEC' },
    { a: 2.7, r: 0.22, label: 'EDGE' }
  ];
  function resize() {
    var size = canvas.clientWidth || 280;
    var dpr = window.devicePixelRatio || 1;
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function draw() {
    var w = canvas.clientWidth || canvas.width;
    var h = canvas.clientHeight || canvas.height;
    var cx = w / 2, cy = h / 2, r = Math.min(w, h) / 2 - 10;

    ctx.clearRect(0, 0, w, h);

    /* 外圈刻度 */
    ctx.strokeStyle = 'rgba(0, 240, 255, .45)';
    ctx.lineWidth = 1;
    for (var t = 0; t < 72; t += 1) {
      var ta = (t / 72) * Math.PI * 2;
      var major = t % 6 === 0;
      var len = major ? 8 : 4;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(ta) * (r + 2), cy + Math.sin(ta) * (r + 2));
      ctx.lineTo(cx + Math.cos(ta) * (r + 2 + len), cy + Math.sin(ta) * (r + 2 + len));
      ctx.stroke();
    }

    /* 距离环 */
    ctx.strokeStyle = 'rgba(0, 240, 255, .22)';
    for (var i = 1; i <= 4; i += 1) {
      ctx.beginPath();
      ctx.arc(cx, cy, (r / 4) * i, 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.beginPath();
    ctx.moveTo(cx - r, cy); ctx.lineTo(cx + r, cy);
    ctx.moveTo(cx, cy - r); ctx.lineTo(cx, cy + r);
    ctx.stroke();

    /* 扫描扇形 + 拖尾 */
    var tail = 0.9;
    for (var k = 0; k < 14; k += 1) {
      var aa = angle - (k / 14) * tail;
      var alpha = 0.16 * (1 - k / 14);
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, r, aa - 0.03, aa);
      ctx.closePath();
      ctx.fillStyle = 'rgba(0, 240, 255, ' + alpha + ')';
      ctx.fill();
    }
    var lead = ctx.createLinearGradient(cx, cy, cx + Math.cos(angle) * r, cy + Math.sin(angle) * r);
    lead.addColorStop(0, 'rgba(0, 240, 255, 0)');
    lead.addColorStop(1, 'rgba(0, 240, 255, .85)');
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(angle) * r, cy + Math.sin(angle) * r);
    ctx.strokeStyle = lead;
    ctx.lineWidth = 2;
    ctx.stroke();

    /* 目标光点：扫到时高亮 */
    targets.forEach(function (target) {
      var tx = cx + Math.cos(target.a) * r * target.r;
      var ty = cy + Math.sin(target.a) * r * target.r;
      var delta = Math.abs(((angle - target.a + Math.PI * 3) % (Math.PI * 2)) - Math.PI);
      var lit = Math.max(0, 1 - delta / 0.9);
      var size = 2 + lit * 3;
      ctx.beginPath();
      ctx.arc(tx, ty, size, 0, Math.PI * 2);
      ctx.fillStyle = lit > 0.15 ? 'rgba(255, 42, 74, ' + (0.35 + lit * 0.65) + ')' : 'rgba(0, 240, 255, .55)';
      ctx.shadowColor = lit > 0.15 ? 'rgba(255, 42, 74, .9)' : 'rgba(0, 240, 255, .6)';
      ctx.shadowBlur = 6 + lit * 12;
      ctx.fill();
      ctx.shadowBlur = 0;
      if (lit > 0.5) {
        ctx.fillStyle = 'rgba(255, 42, 74, .9)';
        ctx.font = '9px "JetBrains Mono", monospace';
        ctx.fillText(target.label, tx + 5, ty - 4);
      }
    });

    /* 中心 */
    ctx.beginPath();
    ctx.arc(cx, cy, 3, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(0, 240, 255, .9)';
    ctx.fill();

    if (azimuth) {
      azimuth.textContent = (Math.round(angle * 180 / Math.PI) % 360).toString().padStart(3, '0') + '°';
    }
    angle += 0.014;
    requestAnimationFrame(draw);
  }
  resize();
  window.addEventListener('resize', resize);
  draw();
})();

/* ---------- 双语切换 ---------- */
(function () {
  var button = document.getElementById('langToggleBtn');
  var current = document.getElementById('langCurrent');
  var alt = document.getElementById('langAlt');
  if (!button || !window.SITE_I18N) { return; }
  var lang = 'zh';
  function apply() {
    var dict = window.SITE_I18N[lang] || {};
    document.querySelectorAll('[data-bind]').forEach(function (node) {
      var value = dict[node.getAttribute('data-bind')];
      if (typeof value === 'string') { node.textContent = value; }
    });
    if (current) { current.textContent = lang.toUpperCase(); }
    if (alt) { alt.textContent = lang === 'zh' ? 'EN' : 'ZH'; }
  }
  button.addEventListener('click', function () {
    lang = lang === 'zh' ? 'en' : 'zh';
    apply();
  });
  apply();
})();

/* ---------- 终端输入 ---------- */
(function () {
  var input = document.getElementById('termInput');
  var output = document.getElementById('termOutput');
  if (!input || !output) { return; }
  var commands = (window.SITE_CONTENT && window.SITE_CONTENT.terminal && window.SITE_CONTENT.terminal.commands) || {};
  function write(text, tone) {
    var line = document.createElement('div');
    line.className = 'term-line' + (tone ? ' ' + tone : '');
    line.textContent = text;
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;
  }
  input.addEventListener('keydown', function (event) {
    if (event.key !== 'Enter') { return; }
    var raw = input.value.trim();
    if (!raw) { return; }
    input.value = '';
    write('duk@agent-ops ~ ' + raw, 'ok');
    var key = raw.toLowerCase();
    if (key === 'clear') { output.innerHTML = ''; return; }
    if (commands[key]) {
      write(commands[key], 'warn');
    } else {
      write("未知命令。输入 'help' 查看可用命令。", 'err');
    }
  });
})();
