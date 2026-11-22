/*
 * The cast box on the home pages. It asks the hosted server (POST /mcp, tool
 * "cast") for a reading and shows the hexagram and the texts the rules select.
 * The question never leaves the browser: it is only shown back and put in the
 * text people can copy into their AI. No AI is called from this page.
 */
(function () {
  "use strict";

  var ENDPOINT = location.hostname === "wengua.allo.land" ? "/mcp" : "https://wengua.allo.land/mcp";

  var UI = {
    en: {
      question: "Your question (optional)",
      placeholder: "What should I understand about…",
      privacy: "Your question stays in your browser. It is not sent anywhere.",
      coins: "Three coins",
      yarrow: "Yarrow stalks",
      cast: "Cast",
      again: "Cast again",
      casting: "Casting…",
      error: "The cast didn't go through. Please try again in a moment.",
      changing: function (n) { return n.length ? "Changing lines: " + n.join(", ") : "No changing lines"; },
      relating: "becomes",
      rule: "Which texts to read",
      judgment: "Judgment",
      line: function (p) { return "Line " + p; },
      use: "All lines",
      legge: "James Legge, 1882",
      moreTitle: "Want more? Use Wengua inside your AI",
      moreBody: "This page casts and shows the classical texts. For an interpretation that connects them to your question, and a conversation about it, add Wengua to the AI you already use. It's free and needs no account.",
      claude: "Add to Claude",
      chatgpt: "Add to ChatGPT",
      all: "All AI apps",
      copy: "Copy this reading for your AI",
      copied: "Copied. Paste it into any AI chat.",
      cast_by: function (m) { return "Cast by the Wengua server with " + (m === "yarrow" ? "the yarrow-stalk method" : "three coins") + " and a secure random generator. Nothing is stored."; },
      asked: "Question: ",
      prompt: "Please interpret this I Ching reading for my question. Quote the texts and keep them apart from your interpretation.",
      links: { claude: "setup/claude/", chatgpt: "setup/chatgpt/", all: "setup/" },
      script: "zh_hant",
    },
    zh: {
      question: "你的问题（可不填）",
      placeholder: "关于……，我应当明白什么？",
      privacy: "问题只留在你的浏览器里，不会发送出去。",
      coins: "三枚铜钱",
      yarrow: "蓍草揲法",
      cast: "起卦",
      again: "再起一卦",
      casting: "起卦中……",
      error: "起卦没有成功，请稍后再试。",
      changing: function (n) { return n.length ? "变爻：" + n.map(function (p) { return "第" + p + "爻"; }).join("、") : "无变爻"; },
      relating: "之",
      rule: "读哪些文字",
      judgment: "卦辞",
      line: function (p) { return "第" + p + "爻"; },
      use: "用爻",
      legge: "理雅各英译，1882",
      moreTitle: "想要更多？在你的 AI 里使用问卦",
      moreBody: "这个页面只负责起卦和显示原文。若想把卦辞和你的问题联系起来解读、继续对话，请把问卦加到你常用的 AI 里。免费，无需注册。",
      claude: "加到 Claude",
      chatgpt: "加到 ChatGPT",
      all: "全部 AI 应用",
      copy: "复制卦象，发给你的 AI",
      copied: "已复制，可粘贴到任何 AI 对话中。",
      cast_by: function (m) { return "由问卦服务器以" + (m === "yarrow" ? "蓍草揲法" : "三枚铜钱") + "和安全随机数起卦，不保存任何内容。"; },
      asked: "问题：",
      prompt: "请为我的问题解读这一卦。引用原文，并把原文和你的解读分开。",
      links: { claude: "setup/#claude", chatgpt: "setup/#chatgpt", all: "setup/" },
      script: "zh_hans",
    },
  };

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function hexName(h, ui) {
    var n = h.name;
    return ui === UI.zh ? "第" + h.number + "卦 " + n.zh_hans : h.number + ". " + n.zh_hant + " " + n.pinyin + " · " + n.en;
  }

  // Six lines, top to bottom; a changing line is marked ○ (old yang) or × (old yin).
  function figure(lines) {
    var f = el("div", "wg-figure");
    lines.slice().reverse().forEach(function (l) {
      var row = el("div", "wg-line" + (l.yang ? " wg-yang" : " wg-yin") + (l.changing ? " wg-changing" : ""));
      row.appendChild(el("span", "wg-bar"));
      if (!l.yang) row.appendChild(el("span", "wg-bar"));
      row.appendChild(el("span", "wg-mark", l.changing ? (l.yang ? "○" : "×") : ""));
      f.appendChild(row);
    });
    return f;
  }

  function hexCard(h, label) {
    var c = el("div", "wg-hex");
    c.appendChild(el("div", "wg-symbol", h.unicode));
    if (label) c.appendChild(el("div", "wg-hexlabel", label));
    return c;
  }

  function textLabel(t, r, ui) {
    var h = t.hexagram === r.primary.number ? r.primary : r.relating;
    var name = ui === UI.zh ? h.name.zh_hans : h.name.zh_hant + " " + h.name.en;
    var what = t.kind === "judgment" ? ui.judgment : t.kind === "use" ? (t.label ? t.label[ui.script] : ui.use) : ui.line(t.position) + (t.label ? " " + t.label[ui.script] : "");
    return name + " · " + what;
  }

  function copyText(r, ui, question) {
    var out = [ui.prompt, ""];
    if (question) out.push(ui.asked + question);
    out.push(hexName(r.primary, ui) + " " + r.primary.unicode + (r.relating ? " → " + hexName(r.relating, ui) + " " + r.relating.unicode : ""));
    out.push(ui.changing(r.changing_lines));
    out.push(r.selection.explanation[ui === UI.zh ? "zh_hans" : "en"]);
    r.selection.texts.forEach(function (t) {
      out.push("");
      out.push(textLabel(t, r, ui) + ": " + t.text[ui.script]);
      if (ui !== UI.zh && t.text.en_legge) out.push(t.text.en_legge + " (Legge)");
    });
    out.push("", "Wengua 问卦 · https://wengua.allo.land");
    return out.join("\n");
  }

  function render(box, r, ui, question) {
    var out = box.querySelector(".wg-result");
    out.textContent = "";

    var head = el("div", "wg-head");
    var pair = el("div", "wg-pair");
    pair.appendChild(figure(r.lines));
    pair.appendChild(hexCard(r.primary, hexName(r.primary, ui)));
    if (r.relating) {
      var to = el("div", "wg-to");
      to.appendChild(el("div", "wg-arrow", ui === UI.zh ? "之" : "→"));
      to.appendChild(hexCard(r.relating, hexName(r.relating, ui)));
      pair.appendChild(to);
    }
    head.appendChild(pair);
    if (question) head.appendChild(el("p", "wg-asked", ui.asked + question));
    head.appendChild(el("p", "wg-changing-text", ui.changing(r.changing_lines)));
    out.appendChild(head);

    out.appendChild(el("h3", null, ui.rule));
    out.appendChild(el("p", "wg-rule", (ui === UI.zh ? r.selection.explanation.zh_hans + "（" + r.selection.source.zh_hans + "）" : r.selection.explanation.en + " (" + r.selection.source.en + ")")));
    r.selection.texts.forEach(function (t) {
      var q = el("blockquote", "wg-text");
      q.appendChild(el("div", "wg-text-label", textLabel(t, r, ui)));
      q.appendChild(el("p", "wg-zh", t.text[ui.script]));
      if (ui !== UI.zh && t.text.en_legge) {
        var en = el("p", "wg-en", t.text.en_legge);
        en.appendChild(el("span", "wg-credit", " (" + ui.legge + ")"));
        q.appendChild(en);
      }
      out.appendChild(q);
    });

    var more = el("div", "wg-more");
    more.appendChild(el("h3", null, ui.moreTitle));
    more.appendChild(el("p", null, ui.moreBody));
    var buttons = el("div", "wg-buttons");
    [["claude", "md-button md-button--primary"], ["chatgpt", "md-button md-button--primary"], ["all", "md-button"]].forEach(function (b) {
      var a = el("a", b[1], ui[b[0]]);
      a.href = ui.links[b[0]];
      buttons.appendChild(a);
    });
    var copy = el("button", "md-button", ui.copy);
    copy.type = "button";
    copy.addEventListener("click", function () {
      var done = function () { copy.textContent = ui.copied; };
      if (navigator.clipboard) navigator.clipboard.writeText(copyText(r, ui, question)).then(done, function () {});
    });
    buttons.appendChild(copy);
    more.appendChild(buttons);
    out.appendChild(more);

    out.appendChild(el("p", "wg-note", ui.cast_by(r.method)));
  }

  function build(box) {
    if (box.dataset.ready) return;
    box.dataset.ready = "1";
    var ui = UI[box.dataset.lang] || UI.en;

    var form = el("form", "wg-form");
    var label = el("label", "wg-qlabel", ui.question);
    var input = el("input", "wg-question");
    input.type = "text";
    input.maxLength = 300;
    input.placeholder = ui.placeholder;
    label.appendChild(input);
    form.appendChild(label);
    form.appendChild(el("p", "wg-privacy", ui.privacy));

    var row = el("div", "wg-row");
    var methods = el("div", "wg-methods");
    ["coins", "yarrow"].forEach(function (m, i) {
      var l = el("label");
      var r = el("input");
      r.type = "radio";
      r.name = "wg-method";
      r.value = m;
      r.checked = i === 0;
      l.appendChild(r);
      l.appendChild(document.createTextNode(" " + ui[m]));
      methods.appendChild(l);
    });
    row.appendChild(methods);
    var go = el("button", "md-button md-button--primary wg-go", ui.cast);
    go.type = "submit";
    row.appendChild(go);
    form.appendChild(row);
    box.appendChild(form);
    var status = el("p", "wg-status");
    status.setAttribute("aria-live", "polite");
    box.appendChild(status);
    box.appendChild(el("div", "wg-result"));

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var method = form.querySelector("input[name=wg-method]:checked").value;
      var question = input.value.trim();
      go.disabled = true;
      status.textContent = ui.casting;
      fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json, text/event-stream" },
        // The question is deliberately not sent.
        body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/call", params: { name: "cast", arguments: { method: method, locale: ui === UI.zh ? "zh-Hans" : "en" } } }),
      })
        .then(function (res) { return res.json(); })
        .then(function (j) {
          var r = j && j.result && j.result.structuredContent;
          if (!r || !r.primary) throw new Error("no reading");
          status.textContent = "";
          render(box, r, ui, question);
          go.textContent = ui.again;
        })
        .catch(function () { status.textContent = ui.error; })
        .then(function () { go.disabled = false; });
    });
  }

  function init() {
    document.querySelectorAll(".wengua-cast").forEach(build);
  }

  // Zensical swaps pages without a reload (instant navigation); document$ fires on each page.
  // Without it, watch the page for a cast box appearing.
  if (window.document$ && window.document$.subscribe) window.document$.subscribe(init);
  else {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
    else init();
    new MutationObserver(init).observe(document.documentElement, { childList: true, subtree: true });
  }
})();
