// src/content.js

const port = chrome.runtime.connect({ name: "sendSiteText" });
port.onMessage.addListener(function(msg) {
  if (msg.flag)

    var allContent = document.getElementsByTagName("html");
    let siteText = "";
    for (const tag of allContent) {
        siteText += "\n" + tag.innerText;
    };

    port.postMessage({ siteText: siteText });
});
