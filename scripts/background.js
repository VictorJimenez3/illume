// once this extension is installed, perform this action
chrome.runtime.onInstalled.addListener(() => {

    // //receiving a message
    // chrome.runtime.onMessage.addListener(
    //     function(request, sender, sendResponse) {
    //     console.log(sender.tab ?
    //                 "from a content script:" + sender.tab.url :
    //                 "from the extension");
    //     if (request.greeting === "hello")
    //         sendResponse({farewell: "goodbye"});
    //     }
    // );

    //create context menu
    chrome.contextMenus.create({
        id: "openSidePanel",
        title: "Show \"%s\" in Side Panel", 
        contexts: ["selection"], 
    })
});

//listener for context menu
// chrome.contextMenus.onClicked.addListener(function(info, tab){
//     //the URL that will be added to based on the selection
//     baseURL = "http://en.wikipedia.org/wiki/";
//     var newURL = baseURL + info.selectionText;
//     //create the new URL in the user's browser
//     chrome.tabs.create({ url: newURL });
// })


// chrome.contextMenus.onClicked.addListener((info, tab) => {
//     if (info.menuItemId === "showInSidePanel" && info.selectionText && tab?.id) {
//       // Step 1: Save selected text — don't await
//       chrome.storage.local.set({ selectedText: info.selectionText }, () => {
//         // Step 2: Immediately open side panel in same callback — preserves user gesture
//         chrome.sidePanel.setOptions({
//           tabId: tab.id,
//           path: "templates/sidepanel.html",
//           enabled: true
//         }, () => {
//           chrome.sidePanel.open({ tabId: tab.id });
//         });
//       });
//     }
//   });

// chrome.contextMenus.onClicked.addListener(function(info, tab) {
//     if (info.menuItemId === "openSidePanel" && info.selectionText) {
//         // Store the selected text in chrome.storage.local for access by the popup
//         chrome.storage.local.set({textSelected: info.selectionText});
//     }
//   });

chrome.contextMenus.onClicked.addListener((info, tab) => {

    if (info.menuItemId === "openSidePanel" && tab?.id) {

        chrome.storage.local.set({selectedText: info.selectionText});

        chrome.sidePanel.setOptions({
            tabId: tab.id,
            path: "templates/sidepanel.html",
            enabled: true
        }, () => {
        chrome.sidePanel.open({ tabId: tab.id });
        });
    }
});
