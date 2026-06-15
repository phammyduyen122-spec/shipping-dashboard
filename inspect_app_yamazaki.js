const fs = require('fs');

// Mock window/localStorage
global.window = {};
global.localStorage = {
    getItem: () => null,
    setItem: () => null
};

// Read data.js
const dataJs = fs.readFileSync('data.js', 'utf8');
eval(dataJs);

const transfers = window.initialTransfers;
console.log(`Loaded ${transfers.length} transfers from data.js.`);

const appJs = fs.readFileSync('app.js', 'utf8');

// Extract linkTransfers function
const linkTransfersMatch = appJs.match(/function linkTransfers[\s\S]*?return \[\.\.\.originals, \.\.\.correctives\];\s*\n?\s*\}/);
if (!linkTransfersMatch) {
    console.log("Could not find linkTransfers in app.js");
    process.exit(1);
}
eval(linkTransfersMatch[0]);

// Extract calculateStatus function
const calculateStatusMatch = appJs.match(/function calculateStatus[\s\S]*?return \{\s*slChuyenKRC[\s\S]*?badgeClass\s*\}\s*;\s*\n?\s*\}/);
if (!calculateStatusMatch) {
    // try another pattern
    const match2 = appJs.match(/function calculateStatus[\s\S]*?statusText,[\s\S]*?badgeClass[\s\S]*?\}/);
    if (match2) {
        eval(match2[0]);
    } else {
        console.log("Could not find calculateStatus in app.js");
        process.exit(1);
    }
} else {
    eval(calculateStatusMatch[0]);
}

// Run linking
const processedTransfers = linkTransfers(transfers);
console.log(`Processed ${processedTransfers.length} transfers.`);

// Filter for Yamazaki items
const codes = ['SP001222', 'SP001988'];
const yamazakiTransfers = processedTransfers.filter(t => codes.includes(t.itemCode));

console.log("\n--- YAMAZAKI TRANSFERS AND CALCULATED STATUS ---");
yamazakiTransfers.forEach(t => {
    // Only print if original with difference, or corrective
    const status = calculateStatus(t);
    const fromB = t.fromBranch;
    const isShortage = fromB === "KHO RAU CỦ" && t.qtyReceived < t.qtyShipped;
    const isCorrective = fromB === "KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG";
    
    if (isShortage || isCorrective || t.matchedCorrectiveQty > 0 || status.statusText !== "Đủ") {
        console.log(`Date: ${t.date} | From: ${t.fromBranch} | To: ${t.toBranch}`);
        console.log(`   Trans: ${t.transferCode} | Code: ${t.itemCode} | Name: ${t.itemName}`);
        console.log(`   Excel Shipped: ${t.qtyShipped} | Excel Received: ${t.qtyReceived} | Matched corrective: ${t.matchedCorrectiveQty || 0}`);
        console.log(`   Calc: slChuyenKRC=${status.slChuyenKRC} | slNhanKRC=${status.slNhanKRC} | slBoSung=${status.slBoSung} | chenhLechConLai=${status.chenhLechConLai} | Status: ${status.statusText}`);
        console.log("--------------------------------------------------");
    }
});
