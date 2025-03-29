// src/content.js

const allContent = document.getElementsByTagName("html");
let siteText = "";
for (const tag of allContent) {
  siteText += "\n" + tag.innerText;
}

const port = chrome.runtime.connect({ name: "sendSiteText" });
port.onMessage.addListener(function(msg) {
  if (msg.flag)
    port.postMessage({ siteText: siteText });
});
