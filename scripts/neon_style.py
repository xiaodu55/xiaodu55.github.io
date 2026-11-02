"""霓虹 Bento 版式的 CSS / JS / HTML 片段。

设计参照用户提供的参考稿 `profile-preview/1.html`：
暗底 #0b0f17、双径向光晕、玻璃拟态卡片（半透明 + 1px 描边 + 20px 圆角 + 背景模糊）、
霓虹青 #00f2fe 强调、胶囊形顶栏、12 栏 Bento 网格、Plus Jakarta Sans + JetBrains Mono、
复制后弹 Toast。

这个文件只放"霓虹"这一套视觉；其余预设仍在 build_site.py 里。
"""

from __future__ import annotations

import html


def esc(text: object) -> str:
    return html.escape(str(text if text is not None else ""), quote=True)


CSS = """/* 霓虹 Bento 版式 · 由 build_site.py 注入 */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --bg: #0b0f17;
  --card-bg: rgba(22, 29, 44, 0.7);
  --card-border: rgba(255, 255, 255, 0.08);
  --card-hover: rgba(30, 41, 63, 0.85);
  --accent-neon: #00f2fe;
  --accent-glow: #4facfe;
  --accent-lime: #a3e635;
  --accent-purple: #c084fc;
  --text-main: #f1f5f9;
  --text-muted: #94a3b8;
  --radius: 20px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background-color: var(--bg);
  color: var(--text-main);
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  min-height: 100vh;
  line-height: 1.6;
  background-image:
    radial-gradient(circle at 15% 20%, rgba(79, 172, 254, 0.12) 0%, transparent 40%),
    radial-gradient(circle at 85% 75%, rgba(163, 230, 53, 0.08) 0%, transparent 45%);
  background-attachment: fixed;
  padding: 1.5rem 1.25rem;
}

.container { max-width: 1120px; margin: 0 auto; }

a { color: var(--accent-neon); }

/* 顶栏 */
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.4rem;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(20px);
  border: 1px solid var(--card-border);
  border-radius: 999px;
  margin-bottom: 2rem;
  gap: 1rem;
  position: sticky;
  top: 1rem;
  z-index: 10;
}

.logo-badge {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  color: var(--text-main);
  font-weight: 700;
  font-size: 1.05rem;
  flex-shrink: 0;
}
.logo-badge .logo-tag {
  background: linear-gradient(135deg, var(--accent-neon), var(--accent-purple));
  color: #0b0f17;
  padding: 0.2rem 0.55rem;
  border-radius: 8px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  font-weight: 800;
}

.nav-links { display: flex; align-items: center; gap: 1.5rem; list-style: none; }
.nav-item a {
  text-decoration: none;
  color: var(--text-muted);
  font-size: 0.92rem;
  font-weight: 600;
  transition: color 0.2s ease;
  position: relative;
  padding-bottom: 4px;
}
.nav-item a:hover { color: var(--text-main); }
.nav-item.active a { color: var(--text-main); }
.nav-item.active a::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0;
  width: 100%; height: 2px;
  background: linear-gradient(90deg, var(--accent-neon), var(--accent-glow));
  border-radius: 2px;
  box-shadow: 0 0 8px var(--accent-neon);
}

.nav-right { display: flex; align-items: center; gap: 0.85rem; flex-shrink: 0; }
.nav-contact-btn {
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-main);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.4rem 0.95rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.04);
  transition: all 0.2s ease;
}
.nav-contact-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: var(--accent-neon);
  color: var(--accent-neon);
}

/* Bento 网格 */
.bento-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 1.25rem; }
.bento-grid > [data-list] { display: contents; }

.card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  backdrop-filter: blur(12px);
  border-radius: var(--radius);
  padding: 1.8rem;
  position: relative;
  overflow: hidden;
  transition: transform 0.25s ease, border-color 0.25s ease, background 0.25s ease;
}
.card:hover {
  transform: translateY(-3px);
  border-color: rgba(255, 255, 255, 0.2);
  background: var(--card-hover);
}

.card-hero { grid-column: span 8; display: flex; flex-direction: column; justify-content: space-between; min-height: 290px; }
.hero-tagline {
  font-size: 0.88rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent-neon);
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: 0.6rem;
  display: flex; align-items: center; gap: 0.5rem;
}
.status-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--accent-lime);
  box-shadow: 0 0 10px var(--accent-lime);
  animation: pulse 2s infinite ease-in-out;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.4; }
}
.hero-title {
  font-size: 2.35rem; line-height: 1.2; font-weight: 800; margin-bottom: 1rem; letter-spacing: -0.02em;
}
.hero-title .hl {
  background: linear-gradient(135deg, #ffffff 40%, var(--accent-neon));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-bio { color: var(--text-muted); font-size: 1.05rem; line-height: 1.65; margin-bottom: 1.5rem; }
.hero-actions { display: flex; gap: 1rem; flex-wrap: wrap; }
.btn {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.65rem 1.25rem; border-radius: 12px;
  font-size: 0.92rem; font-weight: 600; text-decoration: none;
  transition: all 0.2s ease; cursor: pointer; border: 1px solid transparent;
}
.btn-primary { background: var(--text-main); color: #0b0f17; border-color: #ffffff; }
.btn-primary:hover { background: #e2e8f0; box-shadow: 0 0 20px rgba(255, 255, 255, 0.3); }
.btn-ghost { background: rgba(255, 255, 255, 0.05); color: var(--text-main); border-color: var(--card-border); }
.btn-ghost:hover { background: rgba(255, 255, 255, 0.1); }

.card-meta {
  grid-column: span 4;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  text-align: center; gap: 1rem;
}
.avatar-wrapper { position: relative; width: 104px; height: 104px; }
.avatar {
  width: 100%; height: 100%; border-radius: 50%;
  border: 2px solid var(--accent-neon);
  background: #1e293b;
  display: flex; align-items: center; justify-content: center;
  font-size: 2.2rem; font-weight: 800; color: var(--accent-neon);
  box-shadow: 0 0 25px rgba(0, 242, 254, 0.25);
}
.meta-name { font-size: 1.35rem; font-weight: 700; }
.meta-handle { color: var(--accent-neon); font-size: 0.88rem; font-family: 'JetBrains Mono', monospace; margin-top: 0.2rem; }
.meta-chips { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.45rem; }
.chip {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--card-border);
  padding: 0.25rem 0.65rem; border-radius: 8px;
  font-size: 0.8rem; color: var(--text-muted);
}

.card-focus { grid-column: span 7; }
.card-title { font-size: 1.15rem; font-weight: 700; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem; }
.focus-text { color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1.25rem; }
.focus-highlight { color: #38bdf8; font-weight: 600; }
.badge-cloud { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.tech-pill {
  font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;
  padding: 0.35rem 0.75rem; border-radius: 10px;
  background: rgba(56, 189, 248, 0.08);
  border: 1px solid rgba(56, 189, 248, 0.2);
  color: #7dd3fc;
}

.card-highlights { grid-column: span 5; display: flex; flex-direction: column; gap: 0.9rem; }
.card-highlights .highlight-list { display: flex; flex-direction: column; gap: 0.9rem; }
.highlight-item {
  display: flex; align-items: flex-start; gap: 0.75rem;
  padding: 0.6rem; border-radius: 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
}
.highlight-icon { font-size: 1.1rem; line-height: 1.3; }
.highlight-desc { font-size: 0.88rem; color: var(--text-muted); }
.highlight-desc strong { color: var(--text-main); }

.live-card { padding: 1.1rem 1.8rem; }
.live-row { display: flex; flex-wrap: wrap; gap: 2rem; align-items: baseline; }
.live-item { display: flex; align-items: baseline; gap: 0.5rem; }
.live-value { font-family: 'JetBrains Mono', monospace; font-size: 1.35rem; font-weight: 700; color: var(--accent-neon); }
.live-label { font-size: 0.82rem; color: var(--text-muted); }

.stack-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.2rem; }
.stack-group h4 {
  font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; letter-spacing: 0.1em;
  color: var(--accent-neon); margin-bottom: 0.5rem;
}
.stack-group ul { list-style: none; display: grid; gap: 0.3rem; }
.stack-group li { color: var(--text-muted); font-size: 0.86rem; line-height: 1.5; }

.card-contact {
  grid-column: span 12;
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 1.5rem;
  background: linear-gradient(135deg, rgba(22, 29, 44, 0.8) 0%, rgba(30, 41, 63, 0.5) 100%);
}
.contact-cta h3 { font-size: 1.25rem; font-weight: 700; margin-bottom: 0.3rem; }
.contact-cta p { color: var(--text-muted); font-size: 0.9rem; }
.contact-links { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.contact-item {
  display: inline-flex; align-items: center; gap: 0.5rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--card-border);
  padding: 0.6rem 1rem; border-radius: 12px;
  color: var(--text-main); text-decoration: none;
  font-size: 0.88rem; font-family: 'JetBrains Mono', monospace;
  cursor: pointer; transition: all 0.2s ease;
}
.contact-item:hover { background: rgba(255, 255, 255, 0.1); border-color: var(--accent-neon); color: var(--accent-neon); }

/* 内页 */
.page-head { grid-column: span 12; }
.page-head h1 { font-size: 2rem; line-height: 1.25; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.6rem; }
.page-head p { color: var(--text-muted); font-size: 1rem; }
.card-span-12 { grid-column: span 12; }
.card-span-6 { grid-column: span 6; }
.card-span-4 { grid-column: span 4; }

.entry-index {
  font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
  color: var(--accent-neon); letter-spacing: 0.08em;
}
.entry-title { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; margin: 0.35rem 0 0.6rem; }
.entry-title h3 { font-size: 1.12rem; font-weight: 700; }
.entry-title h3 a { color: var(--text-main); text-decoration: none; }
.entry-title h3 a:hover { color: var(--accent-neon); }
.entry-role {
  font-size: 0.76rem; font-family: 'JetBrains Mono', monospace;
  color: #7dd3fc; background: rgba(56, 189, 248, 0.1);
  border: 1px solid rgba(56, 189, 248, 0.22);
  padding: 0.15rem 0.5rem; border-radius: 8px;
}
.entry-summary { color: var(--text-muted); font-size: 0.95rem; }
.entry-label { font-size: 0.8rem; color: var(--text-muted); margin: 0.9rem 0 0.35rem; font-family: 'JetBrains Mono', monospace; }
.entry-list { list-style: none; display: grid; gap: 0.4rem; }
.entry-list li a {
  color: var(--text-muted); text-decoration: none; font-size: 0.9rem;
  display: inline-flex; gap: 0.5rem; align-items: baseline;
}
.entry-list li a:hover { color: var(--accent-neon); }
.entry-list .pr-no { color: var(--accent-neon); font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; }
.entry-all { display: inline-block; margin-top: 0.9rem; font-size: 0.88rem; color: var(--accent-neon); text-decoration: none; }
.entry-all:hover { text-decoration: underline; }

.plain-list { list-style: none; display: grid; gap: 0.35rem; }
.plain-list li a { color: var(--text-muted); text-decoration: none; font-size: 0.92rem; }
.plain-list li a:hover { color: var(--accent-neon); }

.data-note { grid-column: span 12; margin-top: 0.25rem; font-size: 0.8rem; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; line-height: 1.8; }

.toast {
  position: fixed; bottom: 2rem; left: 50%;
  transform: translateX(-50%) translateY(100px);
  background: var(--text-main); color: #0b0f17;
  padding: 0.6rem 1.4rem; border-radius: 999px;
  font-size: 0.9rem; font-weight: 700; opacity: 0;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 100;
}
.toast.show { transform: translateX(-50%) translateY(0); opacity: 1; }

footer {
  text-align: center; margin-top: 3rem;
  color: var(--text-muted); font-size: 0.85rem; font-family: 'JetBrains Mono', monospace;
}

@media (max-width: 900px) {
  header { border-radius: 20px; flex-direction: column; align-items: flex-start; gap: 1rem; position: static; }
  .nav-links { flex-wrap: wrap; gap: 1rem; }
  .nav-right { width: 100%; justify-content: space-between; }
  .card-hero, .card-meta, .card-focus, .card-highlights,
  .card-span-12, .card-span-6, .card-span-4 { grid-column: span 12; }
  .card-contact { flex-direction: column; align-items: flex-start; }
  .hero-title { font-size: 1.9rem; }
}
"""

JS = """// 霓虹 Bento 版式脚本：复制提示 + 读取 content.js 覆盖页面内容
function copyText(text, message) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function () {
      var toast = document.getElementById('toast');
      if (!toast) { return; }
      toast.textContent = message || '已复制';
      toast.classList.add('show');
      setTimeout(function () { toast.classList.remove('show'); }, 1800);
    });
  }
}

document.addEventListener('click', function (event) {
  var button = event.target.closest ? event.target.closest('[data-copy-value]') : null;
  if (button) {
    copyText(button.getAttribute('data-copy-value'), button.getAttribute('data-copy-msg'));
  }
});

/* ---- 内容覆盖：content.js 里的 SITE_CONTENT 会覆盖页面上 data-bind / data-list 标记的内容 ---- */
(function () {
  var data = window.SITE_CONTENT;
  if (!data) { return; }

  function esc(value) {
    return String(value === undefined || value === null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function pick(path) {
    return path.split('.').reduce(function (acc, key) {
      return (acc && typeof acc === 'object') ? acc[key] : undefined;
    }, data);
  }

  function setText(root, path) {
    root.querySelectorAll('[data-bind]').forEach(function (node) {
      var value = pick(node.getAttribute('data-bind'));
      if (typeof value === 'string') { node.textContent = value; }
    });
  }

  var RENDERERS = {
    'home.hero.actions': function (list) {
      return list.map(function (a) {
        var cls = a.primary ? 'btn btn-primary' : 'btn btn-ghost';
        return '<a href="' + esc(a.url || '#') + '" class="' + cls + '"><span>' + esc(a.label) + '</span></a>';
      }).join('');
    },
    'home.meta.chips': function (list) {
      return list.map(function (c) { return '<span class="chip">' + esc(c) + '</span>'; }).join('');
    },
    'home.focus.pills': function (list) {
      return list.map(function (p) { return '<span class="tech-pill"># ' + esc(p) + '</span>'; }).join('');
    },
    'home.highlights.items': function (list) {
      return list.map(function (h) {
        return '<div class="highlight-item"><div class="highlight-icon">' + esc(h.icon || '•') + '</div>' +
          '<div class="highlight-desc"><strong>' + esc(h.title) + '</strong><br>' + esc(h.desc) + '</div></div>';
      }).join('');
    },
    'home.contact.items': function (list) {
      return list.map(function (c) {
        var icon = c.icon || '', label = c.label || '', value = c.value || '';
        var text = [icon, label, value].filter(Boolean).join(' ');
        if (c.copy) {
          return '<button class="contact-item" type="button" data-copy-value="' + esc(value) + '" data-copy-msg="' + esc(text) + ' 已复制">' +
            '<span>' + esc(text) + '</span></button>';
        }
        if (c.href) {
          return '<a class="contact-item" href="' + esc(c.href) + '"><span>' + esc(text) + '</span></a>';
        }
        return '<span class="contact-item"><span>' + esc(text) + '</span></span>';
      }).join('');
    },
    'open_source.entries': function (list) {
      return list.map(function (entry, index) {
        var prs = (entry.prs || []).map(function (pr) {
          return '<li><a href="' + esc(pr.url || '') + '"><span class="pr-no">#' + esc(pr.number) + '</span>' +
            '<span>' + esc(pr.title) + ' ↗</span></a></li>';
        }).join('');
        return '<section class="card card-span-12">' +
          '<div class="entry-index">' + String(index + 1).padStart(2, '0') + '</div>' +
          '<div class="entry-title"><h3><a href="' + esc(entry.url || ('https://github.com/' + entry.repo)) + '">' + esc(entry.repo) + '</a></h3>' +
          (entry.role ? '<span class="entry-role">' + esc(entry.role) + '</span>' : '') + '</div>' +
          (entry.summary ? '<p class="entry-summary">' + esc(entry.summary) + '</p>' : '') +
          (prs ? '<div class="entry-label">代表 PR</div><ul class="entry-list">' + prs + '</ul>' : '') +
          (entry.all_link ? '<a class="entry-all" href="' + esc(entry.all_link) + '">全部记录 ↗</a>' : '') +
          '</section>';
      }).join('');
    },
    'open_source.repo_index': function (list) {
      return '<ul class="plain-list">' + list.map(function (row) {
        return '<li><a href="' + esc(row.url || '') + '">' + esc(row.repo) + ' ↗</a></li>';
      }).join('') + '</ul>';
    },
    'projects.items': function (list) {
      return list.map(function (item, index) {
        var name = item.url
          ? '<a href="' + esc(item.url) + '">' + esc(item.name) + '</a>'
          : esc(item.name);
        var tags = (item.tags || []).map(function (t) {
          return '<span class="tech-pill"># ' + esc(t) + '</span>';
        }).join('');
        var points = (item.points || []).map(function (p) {
          return '<p class="entry-summary">· ' + esc(p) + '</p>';
        }).join('');
        return '<section class="card card-span-6">' +
          '<div class="entry-index">' + String(index + 1).padStart(2, '0') + '</div>' +
          '<div class="entry-title"><h3>' + name + '</h3></div>' +
          (tags ? '<div class="badge-cloud" style="margin-bottom:0.9rem;">' + tags + '</div>' : '') +
          (item.summary ? '<p class="entry-summary">' + esc(item.summary) + '</p>' : '') + points +
          '</section>';
      }).join('');
    },
    'projects.stack.groups': function (list) {
      return list.map(function (group) {
        var items = (group.items || []).map(function (i) { return '<li>' + esc(i) + '</li>'; }).join('');
        return '<div class="stack-group"><h4>' + esc(group.label || '') + '</h4><ul>' + items + '</ul></div>';
      }).join('');
    },
    'learning.items': function (list) {
      return list.map(function (item, index) {
        var title = item.url
          ? '<a href="' + esc(item.url) + '">' + esc(item.title) + '</a>'
          : esc(item.title);
        return '<section class="card card-span-6">' +
          '<div class="entry-index">' + String(index + 1).padStart(2, '0') + '</div>' +
          '<div class="entry-title"><h3>' + title + '</h3></div>' +
          (item.date ? '<div class="entry-label">' + esc(item.date) + '</div>' : '') +
          (item.summary ? '<p class="entrysummary">' + esc(item.summary) + '</p>' : '') +
          '</section>';
      }).join('');
    }
  };

  function applyLists() {
    document.querySelectorAll('[data-list]').forEach(function (node) {
      var path = node.getAttribute('data-list');
      var list = pick(path);
      var renderer = RENDERERS[path];
      if (Array.isArray(list) && renderer) { node.innerHTML = renderer(list); }
    });
  }

  setText(document, 'root');
  applyLists();

  /* ---- GitHub 实时数据：页面打开时直接问 GitHub，数字永远是当下的 ---- */
  function liveFetch() {
    var live = document.querySelectorAll('[data-live]');
    if (!live.length) { return; }
    var cfg = data.github || {};
    if (!cfg.username) { return; }
    var headers = { 'Accept': 'application/vnd.github+json' };
    if (cfg.token) { headers.Authorization = 'Bearer ' + cfg.token; }

    function set(key, value) {
      document.querySelectorAll('[data-live="' + key + '"]').forEach(function (node) {
        node.textContent = value;
      });
    }

    fetch('https://api.github.com/users/' + encodeURIComponent(cfg.username), { headers: headers })
      .then(function (r) { return r.json(); })
      .then(function (u) {
        if (!u || u.errored) { return; }
        set('followers', u.followers);
        set('publicRepos', u.public_repos);
        set('publicGists', u.public_gists);
      })
      .catch(function () {});

    fetch('https://api.github.com/search/issues?q=' +
      encodeURIComponent('is:pr author:' + cfg.username + ' is:merged') + '&per_page=1', { headers: headers })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res && typeof res.total_count === 'number') { set('mergedPRs', res.total_count); }
      })
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
        set('totalStars', total);
        set('topRepoStars', top);
        set('repoCount', repos.length);
      })
      .catch(function () {});
  }

  liveFetch();
})();
"""


def nav_html(nav: list[dict], current: str) -> str:
    items = []
    for entry in nav:
        active = " active" if entry.get("href") == current else ""
        items.append(f'<li class="nav-item{active}"><a href="{esc(entry.get("href"))}">{esc(entry.get("label"))}</a></li>')
    return "\n          ".join(items)


def shell(
    *,
    page: str,
    title: str,
    description: str,
    nav: list[dict],
    body: str,
    footer: str,
    site: dict,
) -> str:
    brand = site.get("brand") or site.get("title", "")
    initials = site.get("initials") or "".join(word[0] for word in str(brand).split()[:2]).upper() or "GH"
    handle = site.get("handle", "")
    logo_href = site.get("logo_href") or (nav[0]["href"] if nav else "index.html")
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="author" content="{esc(site.get("author", ""))}">
  <link rel="stylesheet" href="assets/site.css">
</head>
<body>
  <div class="container">
    <header>
      <a href="{esc(logo_href)}" class="logo-badge">
        <span class="logo-tag">{esc(initials)}</span>
        <span>{esc(brand)}</span>
      </a>
      <nav>
        <ul class="nav-links">
          {nav_html(nav, page)}
        </ul>
      </nav>
      <div class="nav-right">
        <a href="{esc(site.get("contact_href", "#contact"))}" class="nav-contact-btn">联系方式</a>
      </div>
    </header>

    <main class="bento-grid">
{body}
    </main>

    <footer>
      <p>{esc(footer.get("text", ""))}</p>
    </footer>
  </div>

  <div id="toast" class="toast">已复制到剪贴板</div>
  <script src="assets/content.js"></script>
  <script src="assets/site.js" defer></script>
</body>
</html>
"""
