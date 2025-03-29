const allContent = document.getElementsByTagName("html");

var siteText = "";
for (const tag of allContent) {
    siteText += "\n" + tag.innerText;
} 

var port = chrome.runtime.connect({name: "sendSiteText"});
port.onMessage.addListener(function(msg) {
    if (msg.flag)
        port.postMessage({siteText: siteText});
});