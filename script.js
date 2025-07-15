let allTemplates = [];

async function loadTemplates() {
  const res = await fetch("https://api.imgflip.com/get_memes");
  const data = await res.json();
  allTemplates = data.data.memes;

  const select = document.getElementById("meme-template");
  allTemplates.forEach(meme => {
    const option = document.createElement("option");
    option.value = meme.id;
    option.text = meme.name;
    select.appendChild(option);
  });
}

function extractKeywords(text) {
  const lower = text.toLowerCase();
  const keywords = [];
  if (lower.includes("robot")) keywords.push("futurama");
  if (lower.includes("forest")) keywords.push("one does not simply");
  if (lower.includes("dream")) keywords.push("distracted");
  if (lower.includes("fire")) keywords.push("this is fine");
  if (lower.includes("book")) keywords.push("ancient aliens");
  return keywords;
}

function getBestTemplate(keywords) {
  for (let keyword of keywords) {
    let match = allTemplates.find(t => t.name.toLowerCase().includes(keyword));
    if (match) return match;
  }
  return allTemplates[Math.floor(Math.random() * allTemplates.length)];
}

function autoGenerateText(dream) {
  const parts = dream.split(/[.?!]/).map(s => s.trim()).filter(Boolean);
  return {
    top: parts[0] || "In my dream...",
    bottom: parts[1] || "Then something crazy happened!"
  };
}

function processDream() {
  const text = document.getElementById("dream-input").value;
  if (!text.trim()) return alert("Enter your dream description");

  const keywords = extractKeywords(text);
  const selectedTemplate = getBestTemplate(keywords);
  document.getElementById("meme-template").value = selectedTemplate.id;

  const { top, bottom } = autoGenerateText(text);
  document.getElementById("top-text").value = top;
  document.getElementById("bottom-text").value = bottom;
}

async function generateMeme() {
  const top = document.getElementById("top-text").value;
  const bottom = document.getElementById("bottom-text").value;
  const templateId = document.getElementById("meme-template").value;

  const params = new URLSearchParams({
    template_id: templateId,
    username: "ihsana",
    password: "ihs302@ana",
    text0: top,
    text1: bottom
  });

  const res = await fetch(`https://api.imgflip.com/caption_image?${params}`);
  const data = await res.json();
  if (data.success) {
    document.getElementById("meme-image").src = data.data.url;
  } else {
    alert("Failed to generate meme");
  }
}

function downloadMeme() {
  const url = document.getElementById("meme-image").src;
  if (!url) return alert("Generate the meme first!");

  const a = document.createElement("a");
  a.href = url;
  a.download = "dreamweaver-meme.png";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

loadTemplates();
