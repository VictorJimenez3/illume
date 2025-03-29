const allContent = document.getElementsByTagName("html");
var siteText = "";
for (const tag of allContent) {
    siteText += "\n" + tag.innerText;
} 

// console.log(siteText);