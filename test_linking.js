const fs = require('fs');

// Mock window object
global.window = {};

// Read data.js
const dataJs = fs.readFileSync('data.js', 'utf8');
eval(dataJs); // This populates window.initialTransfers

const transfers = window.initialTransfers;
console.log(`Loaded ${transfers.length} transfers.`);

// Extract linkTransfers from app.js
const appJs = fs.readFileSync('app.js', 'utf8');
// We can eval appJs by mock document, but it's simpler to just define the linkTransfers function or eval it if it doesn't depend on DOM
// Let's copy linkTransfers implementation directly or eval the first part of app.js.
// Let's extract linkTransfers function using regex.
const match = appJs.match(/function linkTransfers[\s\S]*?return originals;\s*\n\s*\}/);
if (!match) {
    console.log("Could not find linkTransfers in app.js");
    process.exit(1);
}
eval(match[0]); // Define linkTransfers in global scope

// Run linkTransfers
const processed = linkTransfers(transfers);
console.log(`Processed ${processed.length} transfers.`);

// Find Orchard Garden and combo 3 (10700)
const orchardCombo3 = processed.filter(t => t.toBranch.includes("Orchard Garden") && t.itemCode === "10700");
console.log("\nOrchard Garden Combo 3 processed transfers:");
orchardCombo3.forEach(t => {
    console.log(`ID: ${t.id}, Date: ${t.date}, Shipped: ${t.qtyShipped}, Received: ${t.qtyReceived}, MatchedCorrective: ${t.matchedCorrectiveQty}, Status: ${t.docStatus}`);
});

// Find all processed transfers with matchedCorrectiveQty > 0
const withCorrective = processed.filter(t => t.matchedCorrectiveQty > 0);
console.log(`\nTotal transfers with matched corrective quantity > 0: ${withCorrective.length}`);
if (withCorrective.length > 0) {
    console.log("Sample matched correctives:");
    withCorrective.slice(0, 10).forEach(t => {
        console.log(`ID: ${t.id}, Item: ${t.itemCode}, Branch: ${t.toBranch}, Date: ${t.date}, Shipped: ${t.qtyShipped}, Received: ${t.qtyReceived}, MatchedCorrective: ${t.matchedCorrectiveQty}`);
    });
}
