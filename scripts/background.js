// once this extension is installed, perform this action
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "illume",
        title: "Learn about \"%s\" with illume!", 
        contexts: ["selection"], 
    })
});

let contentPort = null;

chrome.runtime.onConnect.addListener(function(port) {
    if (port.name === "sendSiteText") {
        contentPort = port;

        port.onMessage.addListener(function(msg) {
            if (msg.siteText) {
                console.log("Found site text:");
                console.log(msg.siteText);

                chrome.storage.local.set({ siteText: msg.siteText }, function () {
                    console.log("Site text saved to storage");
                });
            } else {
                console.log("no siteText found");
            }
        });
    }
});


chrome.contextMenus.onClicked.addListener(function(info, tab) {
    if (contentPort) {
        contentPort.postMessage({ flag: "irrelavent" });
    } else {
        console.warn("No connected content script to send message to.");
    }

    // optional: do something with info.selectionText
});

