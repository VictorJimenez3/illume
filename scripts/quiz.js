document.addEventListener('DOMContentLoaded', function() {
    // Tell the background script to change the side panel
    document.getElementById("submit").addEventListener("click", () => {
        //TODO ADD LOCAL VARIABLES AND SEND MESSAGES TO SIDEPANEL SCOPE TO ALLOW FOR SIDEPANEL UPDATE
        window.close();
    });
});