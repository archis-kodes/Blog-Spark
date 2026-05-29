/* ============================================================
   BlogSpark — app.js
   Calls POST 127.0.0.1:8000/blogs, renders Markdown response
   ============================================================ */

const topicInput   = document.getElementById('topic-input');
const generateBtn  = document.getElementById('generate-btn');
const loader       = document.getElementById('loader');
const resultCard   = document.getElementById('result-card');
const blogTitle    = document.getElementById('blog-title');
const blogContent  = document.getElementById('blog-content');
const errorCard    = document.getElementById('error-card');
const errorMsg     = document.getElementById('error-msg');

// ── Allow Enter key (Shift+Enter for newline) to trigger generate ──
topicInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    generateBlog();
  }
});

// ── Main generate function ─────────────────────────────────────────
async function generateBlog() {
  const topic = topicInput.value.trim();

  if (!topic) {
    shakeBorder(topicInput);
    topicInput.focus();
    return;
  }

  setState('loading');

  try {
    const response = await fetch('http://127.0.0.1:8000/blogs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic }),
    });

    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }

    const json = await response.json();

    // Safely extract title and content
    const title   = json?.data?.title   || 'Untitled Blog';
    const content = json?.data?.content || '_No content returned._';

    showResult(title, content);

  } catch (err) {
    showError(err.message || 'Something went wrong. Please try again.');
  }
}

// ── Render result ──────────────────────────────────────────────────
function showResult(title, markdownContent) {
  blogTitle.textContent = title;

  // Use marked.js to render Markdown → HTML
  if (typeof marked !== 'undefined') {
    blogContent.innerHTML = marked.parse(markdownContent);
  } else {
    // Fallback: plain text with basic line break handling
    blogContent.innerHTML = markdownContent
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/\n/g, '<br/>');
  }

  setState('result');

  // Smooth scroll to result
  resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Show error ─────────────────────────────────────────────────────
function showError(message) {
  errorMsg.textContent = message;
  setState('error');
}

// ── State machine ──────────────────────────────────────────────────
function setState(state) {
  // Hide all dynamic sections first
  loader.classList.add('hidden');
  resultCard.classList.add('hidden');
  errorCard.classList.add('hidden');
  generateBtn.disabled = false;
  generateBtn.querySelector('.btn-text').textContent = 'Generate Blog';
  generateBtn.querySelector('.btn-icon').textContent = '🚀';

  if (state === 'loading') {
    loader.classList.remove('hidden');
    generateBtn.disabled = true;
    generateBtn.querySelector('.btn-text').textContent = 'Generating…';
    generateBtn.querySelector('.btn-icon').textContent = '⏳';
  } else if (state === 'result') {
    resultCard.classList.remove('hidden');
  } else if (state === 'error') {
    errorCard.classList.remove('hidden');
  }
}

// ── Reset back to idle ─────────────────────────────────────────────
function resetState() {
  setState('idle');
  topicInput.focus();
}

// ── Copy blog content to clipboard ────────────────────────────────
function copyContent() {
  const text = `${blogTitle.textContent}\n\n${blogContent.innerText}`;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector('.copy-btn');
    btn.style.background = 'var(--green)';
    btn.title = 'Copied!';
    setTimeout(() => {
      btn.style.background = '';
      btn.title = 'Copy content';
    }, 1800);
  }).catch(() => {
    // Fallback for older browsers
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
  });
}

// ── Shake animation for empty input ───────────────────────────────
function shakeBorder(el) {
  el.style.borderColor = 'var(--coral)';
  el.style.boxShadow   = '3px 3px 0 var(--coral)';
  el.animate(
    [
      { transform: 'translateX(0)' },
      { transform: 'translateX(-6px)' },
      { transform: 'translateX(6px)' },
      { transform: 'translateX(-4px)' },
      { transform: 'translateX(4px)' },
      { transform: 'translateX(0)' },
    ],
    { duration: 350, easing: 'ease-in-out' }
  );
  setTimeout(() => {
    el.style.borderColor = '';
    el.style.boxShadow   = '';
  }, 1200);
}
