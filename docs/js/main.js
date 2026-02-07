const user = "1abhax";
const repo = "CTF";
const branch = "main";
const fallbackDir = "writeups";
const GITHUB_TOKEN = "";

function ghHeaders() {
  const h = { "Accept": "application/vnd.github+json" };
  if (GITHUB_TOKEN) h["Authorization"] = `Bearer ${GITHUB_TOKEN}`;
  return h;
}

function escapeHtml(s) {
  return s
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function isMarkdown(name) {
  return name.toLowerCase().endsWith(".md") || name.toLowerCase().endsWith(".markdown");
}

function renderTextAsPre(text) {
  return `<pre>${escapeHtml(text)}</pre>`;
}

function setContentLoading(path) {
  document.getElementById("content").innerHTML = 
    `<div class="loading">⏳ 載入中: ${escapeHtml(path)}</div>`;
}

function setContentError(msg) {
  document.getElementById("content").innerHTML = 
    `<div class="error">❌ ${escapeHtml(msg)}</div>`;
}

async function fetchJson(url) {
  const res = await fetch(url, { headers: ghHeaders() });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  return res.json();
}

async function fetchText(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  return res.text();
}

// 關鍵：使用 raw.githubusercontent.com 訪問檔案
function getRawUrl(path) {
  return `https://raw.githubusercontent.com/${user}/${repo}/${branch}/${path}`;
}

async function loadDir(path = "", container) {
  const url = `https://api.github.com/repos/${user}/${repo}/contents/${encodeURIComponent(path)}?ref=${encodeURIComponent(branch)}`;
  
  const data = await fetchJson(url);
  if (!Array.isArray(data)) return;

  data.sort((a, b) => {
    if (a.type !== b.type) return a.type === "dir" ? -1 : 1;
    return a.name.localeCompare(b.name);
  });

  data.forEach((item) => {
    const div = document.createElement("div");

    if (item.type === "dir") {
      div.className = "folder";
      div.innerHTML = `<span>📁 ${item.name}</span>`;
      
      const sub = document.createElement("div");
      sub.className = "folder-content";
      sub.style.display = "none";
      let loaded = false;

      div.onclick = async (e) => {
        e.stopPropagation();
        
        if (!loaded && !sub.innerHTML.trim()) {
          try {
            sub.style.display = "block";
            sub.innerHTML = `<div class="loading-sub">...</div>`;
            await loadDir(item.path, sub);
            loaded = true;
          } catch (e) {
            sub.innerHTML = `<div class="error-sub">${escapeHtml(String(e.message))}</div>`;
          }
        } else {
          sub.style.display = sub.style.display === "none" ? "block" : "none";
        }
      };

      container.appendChild(div);
      container.appendChild(sub);
    } else {
      div.className = "file";
      div.innerHTML = `<span>📄 ${item.name}</span>`;

      div.onclick = async (e) => {
        e.stopPropagation();
        
        try {
          setContentLoading(item.path);
          const rawUrl = getRawUrl(item.path);
          const text = await fetchText(rawUrl);

          const contentEl = document.getElementById("content");
          if (isMarkdown(item.name) && typeof window.marked !== "undefined") {
            contentEl.innerHTML = `<div class="markdown-content">${window.marked.parse(text)}</div>`;
          } else {
            contentEl.innerHTML = renderTextAsPre(text);
          }
        } catch (e) {
          setContentError(`無法載入: ${String(e.message)}`);
        }
      };

      container.appendChild(div);
    }
  });
}

async function loadConfig() {
  try {
    const res = await fetch("data/config.json");
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return { content_dir: fallbackDir };
  }
}

async function start() {
  const sidebar = document.getElementById("sidebar");
  const content = document.getElementById("content");

  if (!sidebar || !content) {
    console.error("缺少 #sidebar 或 #content");
    return;
  }

  sidebar.innerHTML = "";
  content.innerHTML = `<div class="welcome">👈 選擇檔案查看</div>`;

  try {
    const config = await loadConfig();
    const dir = config.content_dir || fallbackDir;
    await loadDir(dir, sidebar);
  } catch (e) {
    sidebar.innerHTML = `<div class="error">${escapeHtml(String(e.message))}</div>`;
  }
}

start();