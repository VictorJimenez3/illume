// src/background.js

chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
      id: "openSidePanel",
      title: 'Learn about "%s" with illume!',
      contexts: ["selection"]
    });
  });
  
  let contentPort = null;
  
  chrome.runtime.onConnect.addListener((port) => {
    if (port.name === "sendSiteText") {
      contentPort = port;

      console.log("Connected to content script");
  
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
  
  chrome.contextMenus.onClicked.addListener((info, tab) => {

  

    // content port logic setup
    if (contentPort) {
      contentPort.postMessage({ flag: "irrelavent" });
    } else {
      console.warn("No connected content script to send message to.");
    }


    // chrome context menus sidepanel open
    if (info.menuItemId === "openSidePanel" && tab?.id) {

        chrome.storage.local.set({selectedText: info.selectionText});

        // clear quiz_questions storage
        chrome.storage.local.remove(["quiz_questions"], function() {
            console.log("quiz_questions cleared");
        });

        chrome.sidePanel.setOptions({
            tabId: tab.id,
            path: "sidepanel.html",
            enabled: true
        }, () => {
            chrome.sidePanel.open({ tabId: tab.id });
        });
    }
  });
  