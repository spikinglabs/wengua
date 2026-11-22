/*
 * The cast box on the home pages. It asks the hosted server (POST /mcp, tool
 * "cast") for a reading and shows the hexagram and the texts the rules select.
 * The question never leaves the browser: it is only shown back and put in the
 * text people can copy into their AI. No AI is called from this page.
 *
 * The language follows the page: data-lang on the box, else <html lang>.
 * "en" shows traditional Chinese with Legge's English; "zh-hans" and
 * "zh-hant" show the Chinese only, in that script.
 */
(function () {
  "use strict";

  var ENDPOINT = location.hostname === "wengua.allo.land" ? "/mcp" : "https://wengua.allo.land/mcp";

  // Setup guides, relative to the language's home page.
  var LINKS = { claude: "setup/claude/", chatgpt: "setup/chatgpt/", all: "setup/" };

  var UI = {
    en: {
      script: "zh_hant", expl: "en", locale: "en", english: true,
      question: "Your question (optional)",
      placeholder: "What should I understand about…",
      privacy: "Stays in your browser. Nothing is sent or stored.",
      coins: "Three coins", yarrow: "Yarrow stalks",
      cast: "Cast", again: "Cast again", casting: "Casting…",
      error: "The cast didn't go through. Please try again in a moment.",
      changing: function (n) { return n.length ? "Changing lines: " + n.join(", ") : "No changing lines"; },
      name: function (h) { return [h.number + " " + h.name.zh_hant, h.name.pinyin + " · " + h.name.en]; },
      flat: function (h) { return h.number + ". " + h.name.zh_hant + " " + h.name.pinyin + " (" + h.name.en + ")"; },
      textName: function (h) { return h.name.zh_hant + " " + h.name.en; },
      rule: "Texts to read",
      judgment: "Judgment",
      line: function (p) { return "Line " + p; },
      legge: "James Legge, 1882",
      asked: "Question: ",
      moreTitle: "Want more? Use Wengua inside your AI",
      moreBody: "This page casts and shows the classical texts. For an interpretation that connects them to your question, and a conversation about it, add Wengua to the AI you already use. Free, no account.",
      claude: "Add to Claude", chatgpt: "Add to ChatGPT", all: "All AI apps",
      copy: "Copy reading for your AI", copied: "Copied. Paste it into any AI chat.",
      note: function (m) { return "Cast by the Wengua server with " + (m === "yarrow" ? "yarrow stalks" : "three coins") + " and a secure random generator."; },
      prompt: "Please interpret this I Ching reading for my question. Quote the texts and keep them apart from your interpretation.",
    },
    "zh-hans": {
      script: "zh_hans", expl: "zh_hans", locale: "zh-Hans",
      question: "你的问题（可不填）",
      placeholder: "关于……，我应当明白什么？",
      privacy: "只留在你的浏览器里，不发送，不保存。",
      coins: "三枚铜钱", yarrow: "蓍草揲法",
      cast: "起卦", again: "再起一卦", casting: "起卦中……",
      error: "起卦没有成功，请稍后再试。",
      changing: function (n) { return n.length ? "变爻：" + n.map(function (p) { return "第" + p + "爻"; }).join("、") : "无变爻"; },
      name: function (h) { return [h.name.zh_hans, "第" + h.number + "卦"]; },
      flat: function (h) { return "第" + h.number + "卦 " + h.name.zh_hans; },
      textName: function (h) { return h.name.zh_hans; },
      rule: "读哪些文字",
      judgment: "卦辞",
      line: function (p) { return "第" + p + "爻"; },
      asked: "问题：",
      moreTitle: "想要更多？在你的 AI 里使用问卦",
      moreBody: "这个页面只负责起卦和显示原文。若想把原文和你的问题联系起来解读、继续对话，请把问卦加到你常用的 AI 里。免费，无需注册。",
      claude: "加到 Claude", chatgpt: "加到 ChatGPT", all: "全部 AI 应用",
      copy: "复制卦象，发给你的 AI", copied: "已复制，可粘贴到任何 AI 对话中。",
      note: function (m) { return "由问卦服务器以" + (m === "yarrow" ? "蓍草揲法" : "三枚铜钱") + "和安全随机数起卦。"; },
      prompt: "请为我的问题解读这一卦。引用原文，并把原文和你的解读分开。",
    },
    "zh-hant": {
      script: "zh_hant", expl: "zh_hant", locale: "zh-Hant",
      question: "你的問題（可不填）",
      placeholder: "關於……，我應當明白什麼？",
      privacy: "只留在你的瀏覽器裡，不傳送，不儲存。",
      coins: "三枚銅錢", yarrow: "蓍草揲法",
      cast: "起卦", again: "再起一卦", casting: "起卦中……",
      error: "起卦沒有成功，請稍後再試。",
      changing: function (n) { return n.length ? "變爻：" + n.map(function (p) { return "第" + p + "爻"; }).join("、") : "無變爻"; },
      name: function (h) { return [h.name.zh_hant, "第" + h.number + "卦"]; },
      flat: function (h) { return "第" + h.number + "卦 " + h.name.zh_hant; },
      textName: function (h) { return h.name.zh_hant; },
      rule: "讀哪些文字",
      judgment: "卦辭",
      line: function (p) { return "第" + p + "爻"; },
      asked: "問題：",
      moreTitle: "想要更多？在你的 AI 裡使用問卦",
      moreBody: "這個頁面只負責起卦和顯示原文。若想把原文和你的問題聯繫起來解讀、繼續對話，請把問卦加到你常用的 AI 裡。免費，無需註冊。",
      claude: "加到 Claude", chatgpt: "加到 ChatGPT", all: "全部 AI 應用",
      copy: "複製卦象，發給你的 AI", copied: "已複製，可貼到任何 AI 對話中。",
      note: function (m) { return "由問卦伺服器以" + (m === "yarrow" ? "蓍草揲法" : "三枚銅錢") + "和安全亂數起卦。"; },
      prompt: "請為我的問題解讀這一卦。引用原文，並把原文和你的解讀分開。",
    },
  };

  function pickLang(box) {
    var l = (box.dataset.lang || document.documentElement.lang || "en").toLowerCase();
    if (l === "zh-hant" || l === "zh-tw" || l === "zh-hk") return UI["zh-hant"];
    if (l.indexOf("zh") === 0) return UI["zh-hans"];
    return UI.en;
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  // Six lines drawn top to bottom. `marks` puts ○ (old yang) or × (old yin) next to changing lines.
  function figure(yang, changing) {
    var f = el("div", "wg-figure");
    for (var i = 5; i >= 0; i--) {
      var row = el("div", "wg-line" + (changing && changing[i] ? " wg-changing" : ""));
      var bars = el("span", "wg-bars" + (yang[i] ? "" : " wg-yin"));
      bars.appendChild(el("span"));
      if (!yang[i]) bars.appendChild(el("span"));
      row.appendChild(bars);
      row.appendChild(el("span", "wg-mark", changing && changing[i] ? (yang[i] ? "○" : "×") : ""));
      f.appendChild(row);
    }
    return f;
  }

  function hexColumn(h, yang, changing, ui) {
    var c = el("div", "wg-hex");
    c.appendChild(figure(yang, changing));
    var n = ui.name(h);
    c.appendChild(el("div", "wg-hexname", n[0]));
    c.appendChild(el("div", "wg-hexsub", n[1]));
    return c;
  }

  function textLabel(t, r, ui) {
    var h = t.hexagram === r.primary.number ? r.primary : r.relating;
    var what = t.kind === "judgment" ? ui.judgment : t.kind === "use" ? t.label[ui.script] : ui.line(t.position) + " " + t.label[ui.script];
    return ui.textName(h) + " · " + what;
  }

  function copyText(r, ui, question) {
    var out = [ui.prompt, ""];
    if (question) out.push(ui.asked + question);
    out.push(ui.flat(r.primary) + " " + r.primary.unicode + (r.relating ? " → " + ui.flat(r.relating) + " " + r.relating.unicode : ""));
    out.push(ui.changing(r.changing_lines));
    out.push(r.selection.explanation[ui.expl]);
    r.selection.texts.forEach(function (t) {
      out.push("");
      out.push(textLabel(t, r, ui) + ": " + t.text[ui.script]);
      if (ui.english && t.text.en_legge) out.push(t.text.en_legge + " (Legge)");
    });
    out.push("", "Wengua 问卦 · https://wengua.allo.land");
    return out.join("\n");
  }

  function render(box, r, ui, question) {
    var out = box.querySelector(".wg-result");
    out.textContent = "";

    var yang = r.lines.map(function (l) { return l.yang; });
    var changing = r.lines.map(function (l) { return l.changing; });
    var pair = el("div", "wg-pair");
    pair.appendChild(hexColumn(r.primary, yang, changing, ui));
    if (r.relating) {
      pair.appendChild(el("div", "wg-arrow", "→"));
      var bits = r.relating.binary.split("").map(function (b) { return b === "1"; });
      pair.appendChild(hexColumn(r.relating, bits, null, ui));
    }
    out.appendChild(pair);
    out.appendChild(el("p", "wg-meta", ui.changing(r.changing_lines)));
    if (question) out.appendChild(el("p", "wg-asked", ui.asked + question));

    out.appendChild(el("div", "wg-section", ui.rule));
    out.appendChild(el("p", "wg-rule", r.selection.explanation[ui.expl]));
    r.selection.texts.forEach(function (t) {
      var q = el("div", "wg-text");
      q.appendChild(el("div", "wg-text-label", textLabel(t, r, ui)));
      q.appendChild(el("p", "wg-zh", t.text[ui.script]));
      if (ui.english && t.text.en_legge) {
        var en = el("p", "wg-en", t.text.en_legge);
        en.appendChild(el("span", "wg-credit", " (" + ui.legge + ")"));
        q.appendChild(en);
      }
      out.appendChild(q);
    });

    var more = el("div", "wg-more");
    more.appendChild(el("div", "wg-more-title", ui.moreTitle));
    more.appendChild(el("p", null, ui.moreBody));
    var buttons = el("div", "wg-buttons");
    [["claude", true], ["chatgpt", true], ["all", false]].forEach(function (b) {
      var a = el("a", "md-button" + (b[1] ? " md-button--primary" : ""), ui[b[0]]);
      a.href = (ui.links || LINKS)[b[0]];
      buttons.appendChild(a);
    });
    var copy = el("button", "md-button", ui.copy);
    copy.type = "button";
    copy.addEventListener("click", function () {
      if (navigator.clipboard) navigator.clipboard.writeText(copyText(r, ui, question)).then(function () { copy.textContent = ui.copied; }, function () {});
    });
    buttons.appendChild(copy);
    more.appendChild(buttons);
    out.appendChild(more);

    out.appendChild(el("p", "wg-note", ui.note(r.method)));
  }

  function build(box) {
    if (box.dataset.ready) return;
    box.dataset.ready = "1";
    var ui = pickLang(box);

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
      l.appendChild(el("span", null, ui[m]));
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
        body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/call", params: { name: "cast", arguments: { method: method, locale: ui.locale } } }),
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
