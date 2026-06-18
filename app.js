// Shipping Dashboard Application Logic

// Decompress data from data.js
(function() {
    if (window.compressedTransfers && window.itemCatalog && window.branchesList && window.usersList) {
        console.log("Decompressing data...");
        window.initialTransfers = window.compressedTransfers.map(row => {
            const itemCode = row[4];
            const itemInfo = window.itemCatalog[itemCode] || ["", "", "", ""];
            const fromBranch = row[2] === "XL" ? "KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG" : "KHO RAU CỦ";
            const toBranch = window.branchesList[row[3]] || "";
            const nguoiChia = window.usersList[row[10]] || "";
            
            return {
                id: row[0],
                date: row[1],
                fromBranch: fromBranch,
                toBranch: toBranch,
                itemCode: itemCode,
                itemName: itemInfo[0],
                nganhHang: itemInfo[1],
                unit: itemInfo[2],
                subCategoryLevel3: itemInfo[3] || "",
                qtyShipped: row[5],
                qtyReceived: row[6],
                transferCode: row[7],
                generatedDoc: row[8],
                docStatus: row[9],
                nguoiChia: nguoiChia
            };
        });
        
        window.performanceTransfers = window.compressedPerformance.map(row => {
            const barcode = row[3];
            const itemInfo = window.itemCatalog[barcode] || ["", "", "", ""];
            const noiNhan = window.branchesList[row[4]] || "";
            const nguoiChia = window.usersList[row[23]] || "";
            
            return {
                id: row[0],
                maYeuCau: row[1],
                maPhieu: row[2],
                barcode: barcode,
                tenSanPham: itemInfo[0],
                nganhHang: itemInfo[1],
                donVi: itemInfo[2],
                subCategoryLevel3: itemInfo[3] || "",
                noiNhan: noiNhan,
                qtyYcBanDau: row[5],
                qtyHeThong: row[6],
                qtyThucChia: row[7],
                trangThai: row[8],
                trangThaiPR: row[9],
                trangThaiChuyen: row[10],
                canChia: row[11],
                chotNhan: row[12],
                ngayChuyen: row[13],
                ngayGiaoDuKien: row[14],
                noiChuyen: row[15],
                maPhieuChuyen: row[16],
                ngayCapNhat: row[17],
                nguoiCapNhat: row[18],
                batDauChia: row[19],
                hoanTatChia: row[20],
                slRo: row[21],
                slKien: row[22],
                nguoiChia: nguoiChia
            };
        });
        console.log("Decompression complete. initialTransfers:", window.initialTransfers.length, "performanceTransfers:", window.performanceTransfers.length);
    }
})();

// Helper function to format a set of dates for aggregated CTV rows
function formatActiveDates(dateSet) {
    if (!dateSet || dateSet.size === 0) return "";
    const sorted = Array.from(dateSet).sort();
    const formatDateStr = (dStr) => {
        const parts = dStr.split("-");
        if (parts.length === 3) {
            return `${parts[2]}/${parts[1]}`;
        }
        return dStr;
    };
    if (sorted.length === 1) {
        const parts = sorted[0].split("-");
        if (parts.length === 3) {
            return `${parts[2]}/${parts[1]}/${parts[0]}`;
        }
        return sorted[0];
    }
    return `${formatDateStr(sorted[0])} - ${formatDateStr(sorted[sorted.length - 1])}`;
}

// Helper function to format date from YYYY-MM-DD to DD/MM/YYYY in a timezone-independent way
function formatDateToVN(dateStr) {
    if (!dateStr) return "";
    const parts = dateStr.split("-");
    if (parts.length === 3) {
        return `${parts[2]}/${parts[1]}/${parts[0]}`;
    }
    return dateStr;
}

// Helper function to format numbers to a maximum of 2 decimal places using browser locale formatting
function formatNumber(val) {
    if (val === undefined || val === null || isNaN(val) || val === "") return "0";
    const num = Number(val);
    return num.toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    });
}

// Helper function to format differences to a maximum of 2 decimal places with + or - prefixes
function formatDiffNumber(val) {
    if (val === undefined || val === null || isNaN(val) || val === "" || Number(val) === 0) return "0";
    const num = Number(val);
    const formatted = num.toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    });
    return num > 0 ? `+${formatted}` : formatted;
}


// Helper function for flexible date matching (e.g. "6/6", "06/06", "6/6/2026")
function matchDateQuery(dateStr, query) {
    if (!query) return true;
    if (!dateStr) return false;
    
    const parts = dateStr.split("-");
    if (parts.length !== 3) return dateStr.toLowerCase().includes(query.toLowerCase());
    
    const [year, month, day] = parts;
    const dayInt = parseInt(day, 10).toString();
    const monthInt = parseInt(month, 10).toString();
    
    const format1 = `${day}/${month}/${year}`;
    const format2 = `${dayInt}/${monthInt}/${year}`;
    const format3 = `${day}/${month}`;
    const format4 = `${dayInt}/${monthInt}`;
    
    const qClean = query.trim().toLowerCase();
    
    return format1.includes(qClean) || 
           format2.includes(qClean) || 
           format3.includes(qClean) || 
           format4.includes(qClean) ||
           dateStr.includes(qClean);
}

// Helper function to remove Vietnamese accents/diacritics for search matching
function removeVietnameseTones(str) {
    if (!str) return "";
    str = str.replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g,"a"); 
    str = str.replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g,"e"); 
    str = str.replace(/ì|í|ị|ỉ|ĩ/g,"i"); 
    str = str.replace(/ò|ó|ọ|ỏ|ã|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g,"o"); 
    str = str.replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g,"u"); 
    str = str.replace(/ỳ|ý|ỵ|ỷ|ỹ/g,"y"); 
    str = str.replace(/đ/g,"d");
    str = str.replace(/À|Á|Ạ|Ả|Ã|Â|Ầ|Ấ|Ậ|Ẩ|Ẫ|Ă|Ằ|Ắ|Ặ|Ẳ|Ẵ/g, "A");
    str = str.replace(/È|É|Ẹ|Ẻ|Ẽ|Ê|Ề|Ế|Ệ|Ể|Ễ/g, "E");
    str = str.replace(/Ì|Í|Ị|Ỉ|Ĩ/g, "I");
    str = str.replace(/Ò|Ó|Ọ|Ỏ|Ã|Ô|Ồ|Ố|Ộ|Ổ|Ỗ|Ơ|Ờ|Ớ|Ợ|Ở|Ỡ/g, "O");
    str = str.replace(/Ù|Ú|Ụ|Ủ|Ũ|Ư|Ừ|Ứ|Ự|Ử|Ữ/g, "U");
    str = str.replace(/Ỳ|Ý|YY|Ỷ|Ỹ/g, "Y");
    str = str.replace(/Đ/g, "D");
    str = str.replace(/\u0300|\u0301|\u0309|\u0303|\u0323/g, ""); // combining accents
    str = str.replace(/\u02C6|\u0306|\u031B/g, ""); // Â, Ă, Ơ, Ư
    return str;
}

// Data representing shipping transfers (loaded from data.js or fallback)
let initialTransfers = window.initialTransfers || [
    { id: 1, date: "2026-05-20", fromBranch: "Tổng kho miền Nam", toBranch: "Chi nhánh Quận 1", itemCode: "SP001", itemName: "Sữa tươi TH True Milk 1L", unit: "Hộp", qtyShipped: 100, qtyReceived: 100 },
    { id: 2, date: "2026-05-21", fromBranch: "Tổng kho miền Nam", toBranch: "Chi nhánh Bình Thạnh", itemCode: "SP002", itemName: "Thịt ba chỉ heo", unit: "Kg", qtyShipped: 50, qtyReceived: 45 },
    { id: 3, date: "2026-05-21", fromBranch: "Chi nhánh Gò Vấp", toBranch: "Chi nhánh Thủ Đức", itemCode: "SP003", itemName: "Bánh mì gối", unit: "Cái", qtyShipped: 80, qtyReceived: 80 },
    { id: 4, date: "2026-05-22", fromBranch: "Tổng kho miền Nam", toBranch: "Chi nhánh Quận 3", itemCode: "SP004", itemName: "Trứng gà ta (vỉ 10 quả)", unit: "Vỉ", qtyShipped: 150, qtyReceived: 148 },
    { id: 5, date: "2026-05-22", fromBranch: "Tổng kho miền Nam", toBranch: "Chi nhánh Gò Vấp", itemCode: "SP005", itemName: "Rau muống sạch hữu cơ", unit: "Bó", qtyShipped: 60, qtyReceived: 62 },
    { id: 6, date: "2026-05-23", fromBranch: "Chi nhánh Bình Thạnh", toBranch: "Chi nhánh Quận 1", itemCode: "SP001", itemName: "Sữa tươi TH True Milk 1L", unit: "Hộp", qtyShipped: 30, qtyReceived: 30 },
    { id: 7, date: "2026-05-23", fromBranch: "Tổng kho miền Nam", toBranch: "Chi nhánh Thủ Đức", itemCode: "SP006", itemName: "Gạo tám thơm 5kg", unit: "Bao", qtyShipped: 40, qtyReceived: 40 },
    { id: 8, date: "2026-05-24", fromBranch: "Tổng kho miền Nam", toBranch: "Chi nhánh Quận 1", itemCode: "SP007", itemName: "Dầu ăn Simply 1L", unit: "Chai", qtyShipped: 120, qtyReceived: 110 },
    { id: 9, date: "2026-05-24", fromBranch: "Chi nhánh Thủ Đức", toBranch: "Chi nhánh Gò Vấp", itemCode: "SP008", itemName: "Nước khoáng Aquafina 500ml", unit: "Chai", qtyShipped: 200, qtyReceived: 200 },
    { id: 10, date: "2026-05-25", fromBranch: "Tổng kho miền Nam", toBranch: "Chi nhánh Bình Thạnh", itemCode: "SP004", itemName: "Trứng gà ta (vỉ 10 quả)", unit: "Vỉ", qtyShipped: 100, qtyReceived: 100 },
    { id: 11, date: "2026-05-25", fromBranch: "Chi nhánh Quận 3", toBranch: "Chi nhánh Quận 1", itemCode: "SP002", itemName: "Thịt ba chỉ heo", unit: "Kg", qtyShipped: 25, qtyReceived: 28 },
    { id: 12, date: "2026-05-26", fromBranch: "Tổng kho miền Nam", toBranch: "Chi nhánh Quận 3", itemCode: "SP001", itemName: "Sữa tươi TH True Milk 1L", unit: "Hộp", qtyShipped: 80, qtyReceived: 80 },
    { id: 13, date: "2026-05-26", fromBranch: "Tổng kho miền Nam", toBranch: "Chi nhánh Thủ Đức", itemCode: "SP005", itemName: "Rau muống sạch hữu cơ", unit: "Bó", qtyShipped: 70, qtyReceived: 65 },
    { id: 14, date: "2026-05-27", fromBranch: "Chi nhánh Bình Thạnh", toBranch: "Chi nhánh Gò Vấp", itemCode: "SP003", itemName: "Bánh mì gối", unit: "Cái", qtyShipped: 50, qtyReceived: 50 },
    { id: 15, date: "2026-05-27", fromBranch: "Tổng kho miền Nam", toBranch: "Chi nhánh Quận 1", itemCode: "SP006", itemName: "Gạo tám thơm 5kg", unit: "Bao", qtyShipped: 30, qtyReceived: 27 },
];

// Master Item List for Quick Selector & Auto-fill (will be dynamically appended from loaded data)
const masterItems = {
    "SP001": { name: "Sữa tươi TH True Milk 1L", unit: "Hộp" },
    "SP002": { name: "Thịt ba chỉ heo", unit: "Kg" },
    "SP003": { name: "Bánh mì gối", unit: "Cái" },
    "SP004": { name: "Trứng gà ta (vỉ 10 quả)", unit: "Vỉ" },
    "SP005": { name: "Rau muống sạch hữu cơ", unit: "Bó" },
    "SP006": { name: "Gạo tám thơm 5kg", unit: "Bao" },
    "SP007": { name: "Dầu ăn Simply 1L", unit: "Chai" },
    "SP008": { name: "Nước khoáng Aquafina 500ml", unit: "Chai" }
};

// Pre-process and merge transfers (link corrective rows to original rows)
function linkTransfers(rawTransfers) {
    const originals = [];
    const correctives = [];

    // Helper functions for normalization and safe comparison
    const norm = (str) => (str || "").toString().normalize("NFC").trim().toLowerCase();

    rawTransfers.forEach(t => {
        const status = norm(t.docStatus);
        if (status.includes("hủy") || status.includes("huy")) {
            return; // Skip canceled transfers
        }
        
        const fromB = norm(t.fromBranch);
        if (fromB === "kho rau củ") {
            let qtyRec = t.qtyReceived;
            if (qtyRec > t.qtyShipped && qtyRec !== -1) {
                qtyRec = t.qtyShipped;
            }
            originals.push({
                ...t,
                qtyReceived: qtyRec,
                matchedCorrectiveQty: 0
            });
        } else if (fromB === "kho rau củ xử lý chênh lệch chuyển hàng") {
            correctives.push({
                ...t,
                isMerged: false
            });
        }
    });

    const correctiveMap = {};
    correctives.forEach(c => {
        const key = `${norm(c.toBranch)}_${norm(c.itemCode)}`;
        if (!correctiveMap[key]) {
            correctiveMap[key] = [];
        }
        correctiveMap[key].push(c);
    });

    // Pass 1: Match by generatedDoc code link (highest priority)
    originals.forEach(orig => {
        const key = `${norm(orig.toBranch)}_${norm(orig.itemCode)}`;
        const candidates = correctiveMap[key];
        if (candidates && orig.generatedDoc) {
            const origGen = norm(orig.generatedDoc);
            const match = candidates.find(c => {
                if (c.isMerged) return false;
                const cCode = norm(c.transferCode);
                return cCode !== "" && origGen.includes(cCode);
            });
            if (match) {
                orig.matchedCorrectiveQty = match.qtyShipped;
                match.isMerged = true;
            }
        }
    });

    // Pass 2: Fallback matches prioritizing date proximity (0 days first, then up to 3 days)
    for (let maxDiff = 0; maxDiff <= 3; maxDiff++) {
        originals.forEach(orig => {
            if (orig.matchedCorrectiveQty > 0) return; // Already matched
            if (orig.qtyShipped <= orig.qtyReceived) return; // No shortfall
            
            const key = `${norm(orig.toBranch)}_${norm(orig.itemCode)}`;
            const candidates = correctiveMap[key];
            if (candidates) {
                const origDate = new Date(orig.date);
                const match = candidates.find(c => {
                    if (c.isMerged) return false;
                    const cDate = new Date(c.date);
                    const diffDays = Math.abs(cDate - origDate) / (1000 * 60 * 60 * 24);
                    return diffDays <= maxDiff && c.qtyShipped > 0;
                });
                if (match) {
                    orig.matchedCorrectiveQty = match.qtyShipped;
                    match.isMerged = true;
                }
            }
        });
    }

    return [...originals, ...correctives];
}

// State Variables
let transfers = [];
let filteredTransfers = [];
let lastActiveTransfers = [];
let selectedItemCodes = []; // Holds selected Item Codes (tags)
let currentTheme = localStorage.getItem("theme") || "light";
let earliestDate = "";
let latestDate = "";

// Performance Tab State Variables
let performanceTransfers = [];
let performanceTransfersMap = {};
let filteredPerfTransfers = [];
let selectedPerfItemCodes = [];
let selectedSummaryProductCodes = [];
let currentPerfPage = 1;
const perfRowsPerPage = 8;
let currentPerfSortColumn = "ngayChuyen";
let currentPerfSortDirection = "asc";

// Pagination State
let currentPage = 1;
const rowsPerPage = 8;

// Sorting State
let currentSortColumn = "itemCode";
let currentSortDirection = "asc";



// Initialization
document.addEventListener("DOMContentLoaded", () => {
    // Load performance transfers dataset, excluding system controller 'Nhan Quang Hiếu'
    const rawPerfTransfers = window.performanceTransfers || [];
    performanceTransfers = rawPerfTransfers.filter(t => {
        const name = (t.nguoiChia || "").trim().toLowerCase().normalize("NFC");
        const excluded = ["nhan quang hiếu", "nhân quang hiếu", "nhan quang hieu", "nhân quang hieu"];
        return name !== "" && !excluded.includes(name);
    });

    // Populate the performance transfers map for fast lookup
    performanceTransfersMap = {};
    performanceTransfers.forEach(p => {
        const key = `${p.maPhieuChuyen}_${p.barcode}`;
        performanceTransfersMap[key] = p;
    });

    // Link raw transfers
    const rawTransfers = window.initialTransfers || initialTransfers;
    const processedTransfers = linkTransfers(rawTransfers);
    transfers = processedTransfers.map(t => {
        if (t.nguoiChia) {
            const name = t.nguoiChia.trim().toLowerCase().normalize("NFC");
            const excluded = ["nhan quang hiếu", "nhân quang hiếu", "nhan quang hieu", "nhân quang hieu"];
            if (name === "" || excluded.includes(name)) {
                t.nguoiChia = "";
            }
        }
        return t;
    });

    // Populate masterItems dynamically from both datasets
    if (Array.isArray(transfers)) {
        transfers.forEach(t => {
            if (t.itemCode && !masterItems[t.itemCode]) {
                masterItems[t.itemCode] = { name: t.itemName, unit: t.unit };
            }
        });
    }
    if (Array.isArray(performanceTransfers)) {
        performanceTransfers.forEach(t => {
            if (t.barcode && !masterItems[t.barcode]) {
                masterItems[t.barcode] = { name: t.tenSanPham, unit: t.donVi };
            }
        });
    }

    // Set theme
    document.documentElement.setAttribute("data-theme", currentTheme);
    updateThemeToggleUI();

    // Find latest and earliest dates in transfers dataset
    latestDate = "";
    earliestDate = "";
    if (transfers.length > 0) {
        const dates = transfers.map(t => t.date).filter(Boolean);
        if (dates.length > 0) {
            latestDate = dates.reduce((max, d) => d > max ? d : max, dates[0]);
            earliestDate = dates.reduce((min, d) => d < min ? d : min, dates[0]);
        }
    }
    if (!latestDate) {
        latestDate = new Date().toISOString().split("T")[0];
    }
    if (!earliestDate) {
        earliestDate = latestDate;
    }

    // Set default date range to cover the entire dataset range (e.g. June 9 to June 10)
    document.getElementById("filterStartDate").value = earliestDate;
    document.getElementById("filterEndDate").value = latestDate;
    if (document.getElementById("perfFilterStartDate")) {
        document.getElementById("perfFilterStartDate").value = earliestDate;
    }
    if (document.getElementById("perfFilterEndDate")) {
        document.getElementById("perfFilterEndDate").value = latestDate;
    }
    if (document.getElementById("catFilterStartDate")) {
        document.getElementById("catFilterStartDate").value = earliestDate;
    }
    if (document.getElementById("catFilterEndDate")) {
        document.getElementById("catFilterEndDate").value = latestDate;
    }
    if (document.getElementById("exportStartDate")) {
        document.getElementById("exportStartDate").value = earliestDate;
    }
    if (document.getElementById("exportEndDate")) {
        document.getElementById("exportEndDate").value = latestDate;
    }

    // Populate Filters
    populateFilterOptions();
    populatePerfFilterOptions();
    
    // Bind Event Listeners
    setupEventListeners();
    setupTabs();
    setupPerfEventListeners();
    setupCategoryEventListeners(earliestDate, latestDate);
    setupExportTabEventListeners(earliestDate, latestDate);
    
    // Initial Render
    applyFiltersAndRender();
    applyPerfFiltersAndRender();
});

// Setup All Event Listeners
function setupEventListeners() {
    // Theme toggle
    document.getElementById("themeToggleBtn").addEventListener("click", toggleTheme);
    
    // Filters change
    document.getElementById("filterItemCode").addEventListener("input", onItemCodeSearchInput);
    document.getElementById("filterItemCode").addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            confirmSelectedSuggestions();
        }
    });
    document.getElementById("itemTagsContainer").addEventListener("click", () => {
        document.getElementById("filterItemCode").focus();
    });
    
    // Bind Custom Multi-select Dropdowns
    setupMultiSelectDropdown("filterStatusContainer");
    setupMultiSelectDropdown("filterFromBranchContainer");
    setupMultiSelectDropdown("filterToBranchContainer");
    setupMultiSelectDropdown("filterCategoryContainer");
    
    document.getElementById("filterStartDate").addEventListener("change", applyFiltersAndRender);
    document.getElementById("filterEndDate").addEventListener("change", applyFiltersAndRender);
    
    // Clear Filters
    document.getElementById("clearFiltersBtn").addEventListener("click", clearFilters);

    // Close item list & dropdowns when clicking outside
    document.addEventListener("click", (e) => {
        if (!e.target.closest("#filterItemCode") && !e.target.closest("#itemDropdownList")) {
            hideItemDropdownList();
        }
        if (!e.target.closest("#newRecordItemCode") && !e.target.closest("#modalItemDropdownList")) {
            hideModalItemDropdownList();
        }
        if (!e.target.closest(".multiselect-container")) {
            document.querySelectorAll(".multiselect-container").forEach(c => c.classList.remove("active"));
        }
    });

    // Open/Close Add Modal
    document.getElementById("btnAddRecord").addEventListener("click", openAddModal);
    document.getElementById("modalCloseBtn").addEventListener("click", closeAddModal);
    document.getElementById("modalCancelBtn").addEventListener("click", closeAddModal);
    
    // Modal Form Auto-fill based on Item Code
    document.getElementById("newRecordItemCode").addEventListener("input", onModalItemCodeInput);
    
    // Submit Form
    document.getElementById("addRecordForm").addEventListener("submit", handleAddRecord);

    // Export button
    document.getElementById("btnExport").addEventListener("click", exportToCSV);

    // Pagination buttons
    document.getElementById("prevPageBtn").addEventListener("click", () => {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    });
    document.getElementById("nextPageBtn").addEventListener("click", () => {
        const totalPages = Math.ceil(filteredTransfers.length / rowsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderTable();
        }
    });

    // Table sorting triggers
    const tableHeaders = document.querySelectorAll("th[data-sort]");
    tableHeaders.forEach(th => {
        th.addEventListener("click", () => {
            const column = th.getAttribute("data-sort");
            if (currentSortColumn === column) {
                currentSortDirection = currentSortDirection === "asc" ? "desc" : "asc";
            } else {
                currentSortColumn = column;
                currentSortDirection = "asc";
            }
            
            // Update UI sorting indicator
            tableHeaders.forEach(header => {
                header.classList.remove("sort-asc", "sort-desc");
            });
            th.classList.add(currentSortDirection === "asc" ? "sort-asc" : "sort-desc");
            
            sortFilteredData();
            renderTable();
        });
    });
}

// Dark/Light Theme Switching
function toggleTheme() {
    currentTheme = currentTheme === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", currentTheme);
    localStorage.setItem("theme", currentTheme);
    updateThemeToggleUI();
}

function updateThemeToggleUI() {
    const toggleIcon = document.getElementById("themeToggleIcon");
    if (currentTheme === "dark") {
        toggleIcon.innerText = "🌙";
    } else {
        toggleIcon.innerText = "☀️";
    }
}

// Calculate status for a given record
function calculateStatus(t) {
    let slChuyenKRC = t.qtyShipped;
    let slNhanKRC = t.qtyReceived;
    
    // Cap original received quantity: SL nhận <= SL chuyển từ kho rau củ
    const norm = (str) => (str || "").toString().normalize("NFC").trim().toLowerCase();
    const fromB = norm(t.fromBranch);
    if (fromB === "kho rau củ" && slNhanKRC > slChuyenKRC && slNhanKRC !== -1) {
        slNhanKRC = slChuyenKRC;
    }

    let chenhLech = 0;
    let slBoSung = 0;
    let chenhLechConLai = 0;

    let statusText = "Đủ";
    let badgeClass = "badge-du-ok";

    // If quantity received is -1, it means the shipment is still in transit
    if (t.qtyReceived === -1) {
        statusText = "Đang chuyển";
        badgeClass = "badge-dang-chuyen";
        
        return {
            slChuyenKRC,
            slNhanKRC,
            chenhLech: 0,
            slBoSung: 0,
            chenhLechConLai: 0,
            diff: 0,
            statusText,
            badgeClass
        };
    }

    const toB = norm(t.toBranch);
    const isCorrective = fromB === "kho rau củ xử lý chênh lệch chuyển hàng";
    const isSupermarket = toB.startsWith("kfm");

    chenhLech = t.qtyReceived - t.qtyShipped;

    if (isCorrective) {
        slBoSung = isSupermarket ? t.qtyShipped : 0;
        chenhLechConLai = chenhLech; // Direct calculation: SL nhận - SL chuyển
    } else {
        slBoSung = t.matchedCorrectiveQty || 0;
        if (chenhLech < 0) {
            // Shortage: < 0. Adding slBoSung (positive) pulls it towards 0.
            chenhLechConLai = chenhLech + slBoSung;
        } else if (chenhLech > 0) {
            // Surplus: > 0. Subtracting slBoSung (positive) pulls it towards 0.
            chenhLechConLai = chenhLech - slBoSung;
        } else {
            chenhLechConLai = 0;
        }
    }

    // Determine status (Thiếu, Đủ, Dư, Hao hụt) based on Chênh lệch còn lại (chenhLechConLai)
    if (chenhLechConLai < 0) {
        if (t.unit && t.unit.toLowerCase() === "kg" && t.qtyShipped > 0 && (Math.abs(chenhLechConLai) / t.qtyShipped) < 0.15) {
            statusText = "Hao hụt";
            badgeClass = "badge-haohut";
        } else {
            statusText = "Thiếu";
            badgeClass = "badge-thieu";
        }
    } else if (chenhLechConLai > 0) {
        statusText = "Dư";
        badgeClass = "badge-du";
    } else {
        statusText = "Đủ";
        badgeClass = "badge-du-ok";
    }

    return {
        slChuyenKRC,
        slNhanKRC,
        chenhLech,
        slBoSung,
        chenhLechConLai,
        diff: chenhLechConLai, // Diff maps to SL chênh lệch còn lại
        statusText,
        badgeClass
    };
}

// Gather unique list values to populate filtering drop-downs
function populateFilterOptions() {
    const fromBranchOptions = document.getElementById("filterFromBranchOptions");
    const toBranchOptions = document.getElementById("filterToBranchOptions");
    const unitOptions = document.getElementById("filterUnitOptions");
    
    if (fromBranchOptions) fromBranchOptions.innerHTML = '';
    if (toBranchOptions) toBranchOptions.innerHTML = '';
    if (unitOptions) unitOptions.innerHTML = '';

    // Get unique branches
    const fromBranches = [...new Set(transfers.map(t => t.fromBranch))].sort();
    const toBranches = [...new Set(transfers.map(t => t.toBranch))].sort();
    const units = [...new Set(transfers.map(t => t.unit).filter(Boolean))].sort();

    // Populate From Branch
    if (fromBranchOptions) {
        fromBranches.forEach(branch => {
            fromBranchOptions.innerHTML += `
                <label class="multiselect-option">
                    <input type="checkbox" value="${branch}"> <span>${branch}</span>
                </label>
            `;
        });
    }
    
    // Populate To Branch
    if (toBranchOptions) {
        toBranches.forEach(branch => {
            toBranchOptions.innerHTML += `
                <label class="multiselect-option">
                    <input type="checkbox" value="${branch}"> <span>${branch}</span>
                </label>
            `;
        });
    }

    // Populate Units
    if (unitOptions) {
        units.forEach(unit => {
            unitOptions.innerHTML += `
                <label class="multiselect-option">
                    <input type="checkbox" value="${unit}"> <span>${unit}</span>
                </label>
            `;
        });
    }
}

// Autocomplete list matching item code search
function onItemCodeSearchInput(e) {
    const searchVal = e.target.value.toLowerCase().trim();
    const listContainer = document.getElementById("itemDropdownList");
    
    if (searchVal === "") {
        hideItemDropdownList();
        return;
    }

    // Filter matching codes (limit suggestion list to 30 for performance)
    const searchValClean = removeVietnameseTones(searchVal);
    const searchValCleanY = searchValClean.replace(/y/g, 'i');
    const matchedCodes = Object.keys(masterItems).filter(code => {
        const nameClean = removeVietnameseTones(masterItems[code].name.toLowerCase());
        const nameCleanY = nameClean.replace(/y/g, 'i');
        return code.toLowerCase().includes(searchVal) || 
               nameClean.includes(searchValClean) || 
               nameCleanY.includes(searchValCleanY);
    }).slice(0, 30);

    if (matchedCodes.length === 0) {
        hideItemDropdownList();
        return;
    }

    listContainer.innerHTML = "";
    
    // Add "Chọn tất cả" checkbox if more than 1 result
    if (matchedCodes.length > 1) {
        const selectAllDiv = document.createElement("div");
        selectAllDiv.className = "dropdown-search-item";
        selectAllDiv.style.borderBottom = "1px solid var(--border-color)";
        selectAllDiv.style.fontWeight = "600";
        selectAllDiv.style.display = "flex";
        selectAllDiv.style.alignItems = "center";
        
        selectAllDiv.innerHTML = `
            <input type="checkbox" id="suggestionSelectAll" style="margin-right: 8px; cursor: pointer; accent-color: var(--color-primary);">
            <label for="suggestionSelectAll" style="cursor: pointer; display: flex; align-items: center; width: 100%;">Chọn tất cả kết quả gợi ý</label>
        `;
        listContainer.appendChild(selectAllDiv);
        
        const selectAllCb = selectAllDiv.querySelector("#suggestionSelectAll");
        selectAllCb.addEventListener("change", (e) => {
            const isChecked = e.target.checked;
            listContainer.querySelectorAll(".suggestion-checkbox").forEach(cb => {
                cb.checked = isChecked;
            });
        });
    }

    // Render each suggestion with a checkbox
    matchedCodes.forEach(code => {
        const div = document.createElement("div");
        div.className = "dropdown-search-item";
        div.style.display = "flex";
        div.style.alignItems = "center";
        
        const isChecked = selectedItemCodes.includes(code) ? "checked" : "";
        
        div.innerHTML = `
            <input type="checkbox" class="suggestion-checkbox" data-code="${code}" ${isChecked} style="margin-right: 8px; cursor: pointer; accent-color: var(--color-primary);">
            <span style="cursor: pointer; flex: 1;">${code} - ${masterItems[code].name}</span>
        `;
        
        div.addEventListener("click", (ev) => {
            if (ev.target.type !== "checkbox") {
                const cb = div.querySelector(".suggestion-checkbox");
                cb.checked = !cb.checked;
            }
            updateSelectAllCheckboxState(listContainer);
        });
        
        listContainer.appendChild(div);
    });

    // Add a confirm action button at the bottom
    const actionDiv = document.createElement("div");
    actionDiv.style.padding = "8px 12px";
    actionDiv.style.borderTop = "1px solid var(--border-color)";
    actionDiv.style.display = "flex";
    actionDiv.style.justifyContent = "space-between";
    actionDiv.style.alignItems = "center";
    actionDiv.style.backgroundColor = "var(--bg-secondary)";
    
    actionDiv.innerHTML = `
        <span style="font-size: 11px; color: var(--text-muted);">Nhấn Enter hoặc click nút</span>
        <button type="button" class="btn btn-primary" id="btnConfirmSuggestions" style="padding: 4px 10px; font-size: 12px; height: auto; line-height: 1;">Xác nhận chọn</button>
    `;
    
    actionDiv.addEventListener("click", (ev) => {
        ev.stopPropagation();
    });
    
    listContainer.appendChild(actionDiv);
    
    actionDiv.querySelector("#btnConfirmSuggestions").addEventListener("click", () => {
        confirmSelectedSuggestions();
    });

    updateSelectAllCheckboxState(listContainer);
    listContainer.style.display = "block";
}

// Helper to update select all checkbox state based on child checkboxes
function updateSelectAllCheckboxState(listContainer) {
    const selectAllCb = listContainer.querySelector("#suggestionSelectAll");
    if (!selectAllCb) return;
    
    const checkboxes = Array.from(listContainer.querySelectorAll(".suggestion-checkbox"));
    const checkedCount = checkboxes.filter(cb => cb.checked).length;
    
    if (checkedCount === 0) {
        selectAllCb.checked = false;
        selectAllCb.indeterminate = false;
    } else if (checkedCount === checkboxes.length) {
        selectAllCb.checked = true;
        selectAllCb.indeterminate = false;
    } else {
        selectAllCb.checked = false;
        selectAllCb.indeterminate = true;
    }
}

// Helper to commit selected checkboxes as tags
function confirmSelectedSuggestions() {
    const listContainer = document.getElementById("itemDropdownList");
    const checkboxes = listContainer.querySelectorAll(".suggestion-checkbox");
    const input = document.getElementById("filterItemCode");
    
    if (checkboxes.length === 0) {
        const searchVal = input.value.toLowerCase().trim();
        if (searchVal !== "") {
            const searchValClean = removeVietnameseTones(searchVal);
            const searchValCleanY = searchValClean.replace(/y/g, 'i');
            const matchedCodes = Object.keys(masterItems).filter(code => {
                const nameClean = removeVietnameseTones(masterItems[code].name.toLowerCase());
                const nameCleanY = nameClean.replace(/y/g, 'i');
                return code.toLowerCase().includes(searchVal) || 
                       nameClean.includes(searchValClean) || 
                       nameCleanY.includes(searchValCleanY);
            });
            if (matchedCodes.length > 0) {
                matchedCodes.forEach(code => {
                    if (!selectedItemCodes.includes(code)) {
                        selectedItemCodes.push(code);
                    }
                });
                renderItemTags();
                applyFiltersAndRender();
                showToast(`Đã chọn nhanh các sản phẩm chứa từ khóa "${input.value}"`);
            }
        }
        input.value = "";
        hideItemDropdownList();
        return;
    }

    let changed = false;
    const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
    checkboxes.forEach(cb => {
        const code = cb.getAttribute("data-code");
        const shouldBeChecked = anyChecked ? cb.checked : true;
        if (shouldBeChecked) {
            if (!selectedItemCodes.includes(code)) {
                selectedItemCodes.push(code);
                changed = true;
            }
        } else {
            if (selectedItemCodes.includes(code)) {
                selectedItemCodes = selectedItemCodes.filter(c => c !== code);
                changed = true;
            }
        }
    });

    if (changed) {
        renderItemTags();
        applyFiltersAndRender();
        showToast("Đã cập nhật lựa chọn sản phẩm");
    }
    
    input.value = "";
    hideItemDropdownList();
}

// Add Item Code Tag to selection
function addItemCodeTag(code) {
    if (!selectedItemCodes.includes(code)) {
        selectedItemCodes.push(code);
        renderItemTags();
        applyFiltersAndRender();
    }
    document.getElementById("filterItemCode").value = "";
    hideItemDropdownList();
}

// Render selected item tags in search field
function renderItemTags() {
    const container = document.getElementById("itemTagsContainer");
    const input = document.getElementById("filterItemCode");
    
    // Clear everything but keep the input field
    container.innerHTML = "";
    
    selectedItemCodes.forEach(code => {
        const tag = document.createElement("span");
        tag.className = "tag";
        tag.innerHTML = `
            ${code}
            <span class="tag-close" data-code="${code}">&times;</span>
        `;
        container.appendChild(tag);
    });
    
    container.appendChild(input);
    input.focus();
    
    // Bind click events on tag delete icons
    container.querySelectorAll(".tag-close").forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const codeToRemove = btn.getAttribute("data-code");
            selectedItemCodes = selectedItemCodes.filter(c => c !== codeToRemove);
            renderItemTags();
            applyFiltersAndRender();
        });
    });
}

function hideItemDropdownList() {
    document.getElementById("itemDropdownList").style.display = "none";
}

// Autocomplete logic for modal form input
function onModalItemCodeInput(e) {
    const searchVal = e.target.value.toLowerCase().trim();
    const listContainer = document.getElementById("modalItemDropdownList");
    const nameInput = document.getElementById("newRecordItemName");
    const unitInput = document.getElementById("newRecordUnit");

    if (searchVal === "") {
        hideModalItemDropdownList();
        nameInput.value = "";
        unitInput.value = "";
        return;
    }

    // Direct match check
    if (masterItems[searchVal.toUpperCase()]) {
        const match = masterItems[searchVal.toUpperCase()];
        nameInput.value = match.name;
        unitInput.value = match.unit;
        hideModalItemDropdownList();
        return;
    }

    const matchedCodes = Object.keys(masterItems).filter(code => 
        code.toLowerCase().includes(searchVal) || 
        masterItems[code].name.toLowerCase().includes(searchVal)
    );

    if (matchedCodes.length === 0) {
        hideModalItemDropdownList();
        return;
    }

    listContainer.innerHTML = "";
    matchedCodes.forEach(code => {
        const div = document.createElement("div");
        div.className = "dropdown-search-item";
        div.innerText = `${code} - ${masterItems[code].name}`;
        div.addEventListener("click", () => {
            document.getElementById("newRecordItemCode").value = code;
            nameInput.value = masterItems[code].name;
            unitInput.value = masterItems[code].unit;
            hideModalItemDropdownList();
        });
        listContainer.appendChild(div);
    });

    listContainer.style.display = "block";
}

function hideModalItemDropdownList() {
    document.getElementById("modalItemDropdownList").style.display = "none";
}

// Clear all active filters
function clearFilters() {
    // Clear tags
    selectedItemCodes = [];
    renderItemTags();
    
    document.getElementById("filterItemCode").value = "";
    document.getElementById("filterStartDate").value = "";
    document.getElementById("filterEndDate").value = "";
    
    // Reset status checkboxes
    document.querySelectorAll("#filterStatusContainer input[type='checkbox']").forEach(cb => cb.checked = false);
    updateSelectLabel(document.getElementById("filterStatusContainer"), document.querySelector("#filterStatusContainer .multiselect-value"));
    
    // Reset branch checkboxes
    document.querySelectorAll("#filterFromBranchContainer input[type='checkbox']").forEach(cb => cb.checked = false);
    updateSelectLabel(document.getElementById("filterFromBranchContainer"), document.querySelector("#filterFromBranchContainer .multiselect-value"));
    
    document.querySelectorAll("#filterToBranchContainer input[type='checkbox']").forEach(cb => cb.checked = false);
    updateSelectLabel(document.getElementById("filterToBranchContainer"), document.querySelector("#filterToBranchContainer .multiselect-value"));
    
    // Reset unit checkboxes
    const filterUnitContainer = document.getElementById("filterUnitContainer");
    if (filterUnitContainer) {
        filterUnitContainer.querySelectorAll("input[type='checkbox']").forEach(cb => cb.checked = false);
        updateSelectLabel(filterUnitContainer, filterUnitContainer.querySelector(".multiselect-value"));
    }

    // Reset category checkboxes
    const filterCategoryContainer = document.getElementById("filterCategoryContainer");
    if (filterCategoryContainer) {
        filterCategoryContainer.querySelectorAll("input[type='checkbox']").forEach(cb => cb.checked = false);
        updateSelectLabel(filterCategoryContainer, filterCategoryContainer.querySelector(".multiselect-value"));
    }
    
    hideItemDropdownList();
    applyFiltersAndRender();
}

// Core filter computation and view updates
function applyFiltersAndRender() {
    const startDateQuery = document.getElementById("filterStartDate").value;
    const endDateQuery = document.getElementById("filterEndDate").value;

    // Read selected statuses from checkboxes
    const selectedStatuses = Array.from(document.querySelectorAll("#filterStatusContainer input[type='checkbox']:checked")).map(cb => cb.value);
    
    // Read selected branches from checkboxes
    const selectedFromBranches = Array.from(document.querySelectorAll("#filterFromBranchOptions input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedToBranches = Array.from(document.querySelectorAll("#filterToBranchOptions input[type='checkbox']:checked")).map(cb => cb.value);
    
    // Read selected units
    const selectedUnits = Array.from(document.querySelectorAll("#filterUnitContainer input[type='checkbox']:checked")).map(cb => cb.value);
    
    // Read selected categories
    const selectedCategories = Array.from(document.querySelectorAll("#filterCategoryContainer input[type='checkbox']:checked")).map(cb => cb.value);

    // Current text query in item search (if any)
    const textQuery = document.getElementById("filterItemCode").value.toLowerCase().trim();

    filteredTransfers = transfers.filter(transfer => {
        // Status calculations
        const statusInfo = calculateStatus(transfer);
        
        // Match items: match if no tags are selected OR if the item's code is in the selectedItemCodes list
        // Also allow matching by the current search text (if user typed something but hasn't pressed select)
        const matchItem = (selectedItemCodes.length === 0 && textQuery === "") || 
            selectedItemCodes.includes(transfer.itemCode) ||
            (textQuery !== "" && (transfer.itemCode.toLowerCase() === textQuery || transfer.itemName.toLowerCase() === textQuery));
        
        // Match status: match if none checked OR if status is in selected list
        const matchStatus = selectedStatuses.length === 0 || selectedStatuses.includes(statusInfo.statusText);
        
        // Match branches
        const matchFromBranch = selectedFromBranches.length === 0 || selectedFromBranches.includes(transfer.fromBranch);
        const matchToBranch = selectedToBranches.length === 0 || selectedToBranches.includes(transfer.toBranch);
        
        // Match units
        const matchUnit = selectedUnits.length === 0 || selectedUnits.includes(transfer.unit);
        
        // Match dates
        const matchStartDate = startDateQuery === "" || transfer.date >= startDateQuery;
        const matchEndDate = endDateQuery === "" || transfer.date <= endDateQuery;
        
        // Match category
        const matchCategory = selectedCategories.length === 0 || selectedCategories.includes(transfer.nganhHang);

        return matchItem && matchStatus && matchFromBranch && matchToBranch && matchStartDate && matchEndDate && matchUnit && matchCategory;
    });

    // Reset pagination to first page after filters change
    currentPage = 1;

    sortFilteredData();
    renderTable();
    updateSumifsSummary();
}

// ============================================================
// Multi-select custom dropdown controller functions
// ============================================================
function setupMultiSelectDropdown(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const select = container.querySelector(".multiselect-select");
    const valText = container.querySelector(".multiselect-value");
    const searchInput = container.querySelector(".multiselect-search-input");
    const selectAllBtn = container.querySelector(".select-all");
    const clearAllBtn = container.querySelector(".clear-all");
    const optionsList = container.querySelector(".multiselect-options-list");

    let filterFn = applyFiltersAndRender;
    if (containerId.includes("cat")) {
        filterFn = renderF1CategoryTable;
    } else if (containerId.includes("perf")) {
        filterFn = applyPerfFiltersAndRender;
    }

    // Toggle dropdown
    select.addEventListener("click", (e) => {
        e.stopPropagation();
        document.querySelectorAll(".multiselect-container").forEach(c => {
            if (c !== container) c.classList.remove("active");
        });
        container.classList.toggle("active");
        
        if (container.classList.contains("active") && searchInput) {
            searchInput.value = "";
            filterDropdownOptions(optionsList, "");
            searchInput.focus();
        }
    });

    // Handle search text filter
    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            filterDropdownOptions(optionsList, e.target.value);
        });
    }

    // Select All
    if (selectAllBtn) {
        selectAllBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            const visibleCheckboxes = Array.from(optionsList.querySelectorAll(".multiselect-option"))
                .filter(opt => opt.style.display !== "none")
                .map(opt => opt.querySelector("input[type='checkbox']"));
            visibleCheckboxes.forEach(cb => cb.checked = true);
            updateSelectLabel(container, valText);
            filterFn();
        });
    }

    // Clear All
    if (clearAllBtn) {
        clearAllBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            const visibleCheckboxes = Array.from(optionsList.querySelectorAll(".multiselect-option"))
                .filter(opt => opt.style.display !== "none")
                .map(opt => opt.querySelector("input[type='checkbox']"));
            visibleCheckboxes.forEach(cb => cb.checked = false);
            updateSelectLabel(container, valText);
            filterFn();
        });
    }

    // Checkbox state change trigger
    optionsList.addEventListener("change", (e) => {
        if (e.target.type === "checkbox") {
            updateSelectLabel(container, valText);
            filterFn();
        }
    });
}

function filterDropdownOptions(optionsList, query) {
    const q = query.toLowerCase().trim();
    const options = optionsList.querySelectorAll(".multiselect-option");
    options.forEach(opt => {
        const text = opt.innerText.toLowerCase();
        if (text.includes(q)) {
            opt.style.display = "flex";
        } else {
            opt.style.display = "none";
        }
    });
}

function updateSelectLabel(container, labelEl) {
    const checked = Array.from(container.querySelectorAll(".multiselect-options-list input[type='checkbox']:checked"));
    let defaultText = "-- Tất cả --";
    if (container.id.includes("Status")) {
        defaultText = "-- Tất cả trạng thái --";
    } else if (container.id.includes("FromBranch")) {
        defaultText = "-- Tất cả nơi chuyển --";
    } else if (container.id.includes("ToBranch")) {
        defaultText = "-- Tất cả nơi nhận --";
    } else if (container.id.includes("Category")) {
        defaultText = "-- Tất cả ngành hàng --";
    }
        
    if (checked.length === 0) {
        labelEl.innerText = defaultText;
    } else if (checked.length === 1) {
        labelEl.innerText = checked[0].nextElementSibling.innerText;
    } else {
        const total = container.querySelectorAll(".multiselect-options-list input[type='checkbox']").length;
        if (checked.length === total) {
            labelEl.innerText = container.id.includes("Status") 
                ? "Tất cả trạng thái" 
                : (container.id.includes("FromBranch") ? "Tất cả nơi chuyển" : (container.id.includes("ToBranch") ? "Tất cả nơi nhận" : "Tất cả ngành hàng"));
        } else {
            labelEl.innerText = `Đã chọn (${checked.length})`;
        }
    }
}

// Sorting logic implementation
function sortFilteredData() {
    filteredTransfers.sort((a, b) => {
        let valA = a[currentSortColumn];
        let valB = b[currentSortColumn];

        // Format adjustments for sorting
        if (currentSortColumn === "status") {
            valA = calculateStatus(a).statusText;
            valB = calculateStatus(b).statusText;
        } else if (currentSortColumn === "diff") {
            valA = calculateStatus(a).diff;
            valB = calculateStatus(b).diff;
        } else if (currentSortColumn === "slChuyenKRC") {
            valA = calculateStatus(a).slChuyenKRC;
            valB = calculateStatus(b).slChuyenKRC;
        } else if (currentSortColumn === "slNhanKRC") {
            valA = calculateStatus(a).slNhanKRC;
            valB = calculateStatus(b).slNhanKRC;
        } else if (currentSortColumn === "chenhLech") {
            valA = calculateStatus(a).chenhLech;
            valB = calculateStatus(b).chenhLech;
        } else if (currentSortColumn === "slBoSung") {
            valA = calculateStatus(a).slBoSung;
            valB = calculateStatus(b).slBoSung;
        }

        // Compare values
        if (typeof valA === "string") {
            return currentSortDirection === "asc" 
                ? valA.localeCompare(valB, "vi") 
                : valB.localeCompare(valA, "vi");
        } else {
            return currentSortDirection === "asc" ? valA - valB : valB - valA;
        }
    });
}



// Table rendering
function renderTable() {
    const tbody = document.getElementById("tableBody");
    tbody.innerHTML = "";

    if (filteredTransfers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="14" style="text-align: center; padding: 40px; color: var(--text-muted);">Không tìm thấy dữ liệu vận chuyển phù hợp</td></tr>`;
        updatePaginationUI(0);
        return;
    }

    // Determine paging boundaries
    const totalPages = Math.ceil(filteredTransfers.length / rowsPerPage);
    if (currentPage > totalPages) currentPage = totalPages;
    if (currentPage < 1) currentPage = 1;

    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = Math.min(startIndex + rowsPerPage, filteredTransfers.length);
    const paginatedData = filteredTransfers.slice(startIndex, endIndex);

    // Build row markups
    paginatedData.forEach(row => {
        const { slChuyenKRC, slNhanKRC, chenhLech, slBoSung, chenhLechConLai, statusText, badgeClass } = calculateStatus(row);
        
        // Date formatting (timezone-independent)
        const formattedDate = formatDateToVN(row.date);

        const slChuyenText = formatNumber(slChuyenKRC);
        const slNhanText = slNhanKRC === -1 ? "-1" : formatNumber(slNhanKRC);
        const chenhLechText = slNhanKRC === -1 ? "0" : formatDiffNumber(chenhLech);
        const slBoSungText = formatNumber(slBoSung);
        const chenhLechConLaiText = slNhanKRC === -1 ? "0" : formatDiffNumber(chenhLechConLai);

        // Difference styling based on status
        const diffStyle = statusText === "Thiếu" 
            ? 'color: var(--color-danger); font-weight: 500;' 
            : (statusText === "Dư" ? 'color: var(--color-info); font-weight: 500;' : (statusText === "Hao hụt" ? 'color: var(--color-warning); font-weight: 500;' : ''));

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${formattedDate}</td>
            <td>${row.fromBranch}</td>
            <td>${row.toBranch}</td>
            <td><span style="font-weight: 500;">${row.nguoiChia || ""}</span></td>
            <td><strong style="color: var(--color-primary);">${row.itemCode}</strong></td>
            <td>${row.itemName}</td>
            <td>${row.unit}</td>
            <td>${row.nganhHang || "Khác"}</td>
            <td style="text-align: right; font-weight: 500;">${slChuyenText}</td>
            <td style="text-align: right; font-weight: 500;">${slNhanText}</td>
            <td style="text-align: right; font-weight: 500;">${chenhLechText}</td>
            <td style="text-align: right; font-weight: 500; color: var(--color-primary);">${slBoSungText}</td>
            <td style="text-align: right; ${diffStyle}">${chenhLechConLaiText}</td>
            <td><span class="badge ${badgeClass}">${statusText}</span></td>
        `;
        tbody.appendChild(tr);
    });

    updatePaginationUI(totalPages, startIndex + 1, endIndex, filteredTransfers.length);
}

// Update Pagination Labels and Buttons
function updatePaginationUI(totalPages, fromIndex = 0, toIndex = 0, totalCount = 0) {
    const prevBtn = document.getElementById("prevPageBtn");
    const nextBtn = document.getElementById("nextPageBtn");
    const infoText = document.getElementById("paginationInfo");

    if (totalCount === 0) {
        prevBtn.disabled = true;
        nextBtn.disabled = true;
        infoText.innerText = "Hiển thị 0 của 0 bản ghi";
        return;
    }

    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages;
    infoText.innerText = `Hiển thị từ ${fromIndex} đến ${toIndex} của ${totalCount.toLocaleString()} bản ghi (Trang ${currentPage}/${totalPages})`;
}



// Modal open actions
function openAddModal() {
    // Clear inputs
    document.getElementById("addRecordForm").reset();
    
    // Set default date to today
    const today = new Date().toISOString().split("T")[0];
    document.getElementById("newRecordDate").value = today;

    // Show modal
    document.getElementById("addRecordModal").classList.add("active");
}

function closeAddModal() {
    document.getElementById("addRecordModal").classList.remove("active");
    hideModalItemDropdownList();
}

// Form submit record handler
function handleAddRecord(e) {
    e.preventDefault();

    const date = document.getElementById("newRecordDate").value;
    const fromBranch = document.getElementById("newRecordFromBranch").value.trim();
    const toBranch = document.getElementById("newRecordToBranch").value.trim();
    const itemCode = document.getElementById("newRecordItemCode").value.toUpperCase().trim();
    const itemName = document.getElementById("newRecordItemName").value.trim();
    const unit = document.getElementById("newRecordUnit").value.trim();
    const qtyShipped = parseFloat(document.getElementById("newRecordQtyShipped").value);
    const qtyReceived = parseFloat(document.getElementById("newRecordQtyReceived").value);

    // Validation checks
    if (!date || !fromBranch || !toBranch || !itemCode || !itemName || !unit || isNaN(qtyShipped) || isNaN(qtyReceived)) {
        alert("Vui lòng nhập đầy đủ và chính xác tất cả thông tin!");
        return;
    }

    if (fromBranch === toBranch) {
        alert("Chi nhánh chuyển và nhận không được trùng nhau!");
        return;
    }

    // Add to Master Items dictionary if it is a new item code
    if (!masterItems[itemCode]) {
        masterItems[itemCode] = { name: itemName, unit: unit };
    }

    // Insert new item in array
    const newId = transfers.length > 0 ? Math.max(...transfers.map(t => t.id)) + 1 : 1;
    const newTransfer = {
        id: newId,
        date,
        fromBranch,
        toBranch,
        itemCode,
        itemName,
        unit,
        qtyShipped,
        qtyReceived
    };

    transfers.unshift(newTransfer); // Add to the front of list

    // Refresh controls and reload UI
    populateFilterOptions();
    closeAddModal();
    applyFiltersAndRender();

    // Visual confirmation notification (simple overlay toast)
    showToast(`Đã thêm vận chuyển cho mã hàng ${itemCode} thành công!`);
}

// Simple dynamic Toast notification
function showToast(message) {
    const toast = document.createElement("div");
    toast.style.position = "fixed";
    toast.style.bottom = "24px";
    toast.style.right = "24px";
    toast.style.backgroundColor = "var(--bg-secondary)";
    toast.style.border = "1px solid var(--color-primary)";
    toast.style.boxShadow = "var(--shadow-premium)";
    toast.style.color = "var(--text-primary)";
    toast.style.padding = "14px 20px";
    toast.style.borderRadius = "var(--radius-md)";
    toast.style.zIndex = "2000";
    toast.style.fontWeight = "600";
    toast.style.fontSize = "14px";
    toast.style.opacity = "0";
    toast.style.transform = "translateY(20px)";
    toast.style.transition = "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)";
    
    toast.innerText = message;
    document.body.appendChild(toast);

    // Trigger transition
    setTimeout(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateY(0)";
    }, 100);

    // Fade out and remove
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(20px)";
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// CSV Export Utility (with BOM encoding to support Excel Vietnamese text)
function exportToCSV() {
    if (filteredTransfers.length === 0) {
        alert("Không có dữ liệu để xuất!");
        return;
    }

    let csvContent = "\uFEFF"; // UTF-8 BOM representation
    csvContent += "Ngày chuyển,Chi nhánh chuyển,Chi nhánh nhận,Người chia,Mã hàng,Tên hàng,Đơn vị tính,Ngành hàng,SL chuyển,SL nhận,Chênh lệch,SL bổ sung,SL chênh lệch còn lại,Trạng thái\n";

    filteredTransfers.forEach(t => {
        const { slChuyenKRC, slNhanKRC, chenhLech, slBoSung, chenhLechConLai, statusText } = calculateStatus(t);
        
        const row = [
            t.date,
            `"${t.fromBranch.replace(/"/g, '""')}"`,
            `"${t.toBranch.replace(/"/g, '""')}"`,
            `"${(t.nguoiChia || "").replace(/"/g, '""')}"`,
            `"${t.itemCode.replace(/"/g, '""')}"`,
            `"${t.itemName.replace(/"/g, '""')}"`,
            `"${t.unit.replace(/"/g, '""')}"`,
            `"${(t.nganhHang || "Khác").replace(/"/g, '""')}"`,
            slChuyenKRC,
            slNhanKRC === -1 ? -1 : slNhanKRC,
            slNhanKRC === -1 ? 0 : chenhLech,
            slBoSung,
            slNhanKRC === -1 ? 0 : chenhLechConLai,
            `"${statusText}"`
        ];
        csvContent += row.join(",") + "\n";
    });

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    
    // File name format with current date
    const todayStr = new Date().toISOString().split("T")[0];
    link.setAttribute("download", `BaoCao_DieuChuyenHang_${todayStr}.csv`);
    link.style.visibility = "hidden";
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Calculate pivot sumifs summary statistics
function updateSumifsSummary() {
    // Calculate total shipped quantity for the unique combinations of (itemCode, date) in filteredTransfers across all branches
    const activeKeys = new Set();
    filteredTransfers.forEach(t => {
        activeKeys.add(`${t.date}_${t.itemCode}`);
    });

    let totalShipped = 0;
    transfers.forEach(t => {
        if (activeKeys.has(`${t.date}_${t.itemCode}`)) {
            totalShipped += t.qtyShipped;
        }
    });

    let duCount = 0, duShipped = 0, duReceived = 0;
    let thieuCount = 0, thieuVal = 0;
    let duThieuCount = 0, duThieuVal = 0;
    let chuyenCount = 0, chuyenShipped = 0;

    filteredTransfers.forEach(t => {
        const { diff, statusText } = calculateStatus(t);
        
        if (statusText === "Đang chuyển") {
            chuyenCount++;
            chuyenShipped += t.qtyShipped;
        } else if (statusText === "Đủ") {
            duCount++;
            duShipped += t.qtyShipped;
            duReceived += t.qtyReceived;
        } else if (statusText === "Thiếu") {
            thieuCount++;
            thieuVal += Math.abs(diff);
        } else if (statusText === "Dư") {
            duThieuCount++;
            duThieuVal += Math.abs(diff);
        }
    });

    // Check if sumifs fields exist in the DOM before writing to avoid JS crashes
    const sumifsTotalShippedEl = document.getElementById("sumifsTotalShipped");
    const sumifsDuCountEl = document.getElementById("sumifsDuCount");
    const sumifsDuQtyEl = document.getElementById("sumifsDuQty");
    const sumifsThieuCountEl = document.getElementById("sumifsThieuCount");
    const sumifsThieuQtyEl = document.getElementById("sumifsThieuQty");
    const sumifsDuThieuCountEl = document.getElementById("sumifsDuThieuCount");
    const sumifsDuThieuQtyEl = document.getElementById("sumifsDuThieuQty");
    const sumifsChuyenCountEl = document.getElementById("sumifsChuyenCount");
    const sumifsChuyenQtyEl = document.getElementById("sumifsChuyenQty");

    if (sumifsTotalShippedEl) sumifsTotalShippedEl.innerText = formatNumber(totalShipped);
    if (sumifsDuCountEl) sumifsDuCountEl.innerText = `${formatNumber(duCount)} đơn`;
    if (sumifsDuQtyEl) sumifsDuQtyEl.innerText = `Chuyển: ${formatNumber(duShipped)} | Nhận: ${formatNumber(duReceived)}`;

    if (sumifsThieuCountEl) sumifsThieuCountEl.innerText = `${formatNumber(thieuCount)} đơn`;
    if (sumifsThieuQtyEl) sumifsThieuQtyEl.innerText = `Tổng lệch thiếu: -${formatNumber(thieuVal)}`;

    if (sumifsDuThieuCountEl) sumifsDuThieuCountEl.innerText = `${formatNumber(duThieuCount)} đơn`;
    if (sumifsDuThieuQtyEl) sumifsDuThieuQtyEl.innerText = `Tổng lệch dư: +${formatNumber(duThieuVal)}`;

    if (sumifsChuyenCountEl) sumifsChuyenCountEl.innerText = `${formatNumber(chuyenCount)} đơn`;
    if (sumifsChuyenQtyEl) sumifsChuyenQtyEl.innerText = `Tổng đang đi: ${formatNumber(chuyenShipped)}`;
}

// Tab Switcher Controller
function setupTabs() {
    const tabTransferMonitor = document.getElementById("tabTransferMonitor");
    const tabPerformanceReport = document.getElementById("tabPerformanceReport");
    const tabCategoryPerformance = document.getElementById("tabCategoryPerformance");
    const tabExportExcel = document.getElementById("tabExportExcel");
    
    const contentTransferMonitor = document.getElementById("contentTransferMonitor");
    const contentPerformanceReport = document.getElementById("contentPerformanceReport");
    const contentCategoryPerformance = document.getElementById("contentCategoryPerformance");
    const contentExportExcel = document.getElementById("contentExportExcel");

    if (!tabTransferMonitor || !tabPerformanceReport || !tabCategoryPerformance) return;

    tabTransferMonitor.addEventListener("click", () => {
        tabTransferMonitor.classList.add("active");
        tabPerformanceReport.classList.remove("active");
        tabCategoryPerformance.classList.remove("active");
        if (tabExportExcel) tabExportExcel.classList.remove("active");
        
        contentTransferMonitor.classList.add("active");
        contentPerformanceReport.classList.remove("active");
        contentCategoryPerformance.classList.remove("active");
        if (contentExportExcel) contentExportExcel.classList.remove("active");
    });

    tabPerformanceReport.addEventListener("click", () => {
        tabPerformanceReport.classList.add("active");
        tabTransferMonitor.classList.remove("active");
        tabCategoryPerformance.classList.remove("active");
        if (tabExportExcel) tabExportExcel.classList.remove("active");
        
        contentPerformanceReport.classList.add("active");
        contentTransferMonitor.classList.remove("active");
        contentCategoryPerformance.classList.remove("active");
        if (contentExportExcel) contentExportExcel.classList.remove("active");
        
        applyPerfFiltersAndRender();
    });

    tabCategoryPerformance.addEventListener("click", () => {
        tabCategoryPerformance.classList.add("active");
        tabTransferMonitor.classList.remove("active");
        tabPerformanceReport.classList.remove("active");
        if (tabExportExcel) tabExportExcel.classList.remove("active");
        
        contentCategoryPerformance.classList.add("active");
        contentTransferMonitor.classList.remove("active");
        contentPerformanceReport.classList.remove("active");
        if (contentExportExcel) contentExportExcel.classList.remove("active");
        
        renderF1CategoryTable();
    });

    if (tabExportExcel && contentExportExcel) {
        tabExportExcel.addEventListener("click", () => {
            tabExportExcel.classList.add("active");
            tabTransferMonitor.classList.remove("active");
            tabPerformanceReport.classList.remove("active");
            tabCategoryPerformance.classList.remove("active");
            
            contentExportExcel.classList.add("active");
            contentTransferMonitor.classList.remove("active");
            contentPerformanceReport.classList.remove("active");
            contentCategoryPerformance.classList.remove("active");
            
            renderExportPreview();
        });
    }
}

// Populate filters drop-down lists for Performance Tab
function populatePerfFilterOptions() {
    const userOptions = document.getElementById("perfFilterUserOptions");
    const toBranchOptions = document.getElementById("perfFilterToBranchOptions");
    const unitOptions = document.getElementById("perfFilterUnitOptions");
    
    if (!userOptions || !toBranchOptions || !unitOptions) return;
    
    userOptions.innerHTML = '';
    toBranchOptions.innerHTML = '';
    unitOptions.innerHTML = '';

    // Get unique sorted values
    const users = [...new Set(performanceTransfers.map(t => t.nguoiChia).filter(Boolean))].sort();
    const toBranches = [...new Set(performanceTransfers.map(t => t.noiNhan).filter(Boolean))].sort();
    const units = [...new Set(transfers.map(t => t.unit).filter(Boolean))].sort();

    // Populate Users list
    users.forEach(user => {
        userOptions.innerHTML += `
            <label class="multiselect-option">
                <input type="checkbox" value="${user}"> <span>${user}</span>
            </label>
        `;
    });
    
    // Populate Receiving branches list
    toBranches.forEach(branch => {
        toBranchOptions.innerHTML += `
            <label class="multiselect-option">
                <input type="checkbox" value="${branch}"> <span>${branch}</span>
            </label>
        `;
    });

    // Populate Units list
    units.forEach(unit => {
        unitOptions.innerHTML += `
            <label class="multiselect-option">
                <input type="checkbox" value="${unit}"> <span>${unit}</span>
            </label>
        `;
    });
}

// Setup Event Listeners for Performance Tab
function setupPerfEventListeners() {
    setupMultiSelectDropdown("perfFilterGroupContainer");
    setupMultiSelectDropdown("perfFilterUserContainer");
    setupMultiSelectDropdown("perfFilterStatusContainer");
    setupMultiSelectDropdown("perfFilterToBranchContainer");
    setupMultiSelectDropdown("perfFilterUnitContainer");
    setupMultiSelectDropdown("perfFilterCategoryContainer");
    
    document.getElementById("perfFilterStartDate").addEventListener("change", applyPerfFiltersAndRender);
    document.getElementById("perfFilterEndDate").addEventListener("change", applyPerfFiltersAndRender);
    document.getElementById("perfClearFiltersBtn").addEventListener("click", clearPerfFilters);
    
    // Item search autocomplete and key listener
    document.getElementById("perfFilterItemCode").addEventListener("input", onPerfItemSearchInput);
    document.getElementById("perfItemTagsContainer").addEventListener("click", () => {
        document.getElementById("perfFilterItemCode").focus();
    });
    
    document.getElementById("perfFilterItemCode").addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            confirmSelectedPerfSuggestions();
        }
    });

    // Summary table item search autocomplete, focus click, and key listener
    const summaryFilterProduct = document.getElementById("perfSummaryFilterProduct");
    if (summaryFilterProduct) {
        summaryFilterProduct.addEventListener("input", onSummaryProductSearchInput);
        const summaryTagsContainer = document.getElementById("perfSummaryItemTagsContainer");
        if (summaryTagsContainer) {
            summaryTagsContainer.addEventListener("click", () => {
                summaryFilterProduct.focus();
            });
        }
        summaryFilterProduct.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                confirmSelectedSummaryProductSuggestions();
            }
        });
    }

    document.addEventListener("click", (e) => {
        if (!e.target.closest("#perfFilterItemCode") && !e.target.closest("#perfItemDropdownList")) {
            hidePerfItemDropdownList();
        }
        if (!e.target.closest("#perfSummaryFilterProduct") && !e.target.closest("#perfSummaryItemDropdownList")) {
            hideSummaryProductDropdownList();
        }
    });

    document.getElementById("perfBtnExport").addEventListener("click", exportPerfToCSV);

    document.getElementById("perfPrevPageBtn").addEventListener("click", () => {
        if (currentPerfPage > 1) {
            currentPerfPage--;
            renderPerfTable();
        }
    });
    document.getElementById("perfNextPageBtn").addEventListener("click", () => {
        const discrepantData = getFilteredPerfDiscrepantData();
        const totalPages = Math.ceil(discrepantData.length / perfRowsPerPage);
        if (currentPerfPage < totalPages) {
            currentPerfPage++;
            renderPerfTable();
        }
    });

    // Inline table filters search inputs
    const tableFilterDate = document.getElementById("perfTableFilterDate");
    const tableFilterUser = document.getElementById("perfTableFilterUser");
    const tableFilterBarcode = document.getElementById("perfTableFilterBarcode");
    const tableFilterName = document.getElementById("perfTableFilterName");
    const tableFilterUnit = document.getElementById("perfTableFilterUnit");
    
    if (tableFilterDate) {
        tableFilterDate.addEventListener("input", () => {
            currentPerfPage = 1;
            renderPerfTable();
        });
    }
    
    if (tableFilterUser) {
        tableFilterUser.addEventListener("input", () => {
            currentPerfPage = 1;
            renderPerfTable();
            renderPerfSummaryTable();
        });
    }
    
    if (tableFilterBarcode) {
        tableFilterBarcode.addEventListener("input", () => {
            currentPerfPage = 1;
            renderPerfTable();
            renderPerfSummaryTable();
        });
    }

    if (tableFilterName) {
        tableFilterName.addEventListener("input", () => {
            currentPerfPage = 1;
            renderPerfTable();
            renderPerfSummaryTable();
        });
    }

    if (tableFilterUnit) {
        tableFilterUnit.addEventListener("input", () => {
            currentPerfPage = 1;
            renderPerfTable();
            renderPerfSummaryTable();
        });
    }

    // Inline filters for summary table
    const summaryFilterDate = document.getElementById("perfSummaryFilterDate");
    const summaryFilterUser = document.getElementById("perfSummaryFilterUser");
    const summaryFilterCategory = document.getElementById("perfSummaryFilterCategory");
    const summaryFilterStatus = document.getElementById("perfSummaryFilterStatus");

    if (summaryFilterDate) {
        summaryFilterDate.addEventListener("input", () => {
            renderPerfSummaryTable();
        });
    }
    if (summaryFilterUser) {
        summaryFilterUser.addEventListener("input", () => {
            renderPerfSummaryTable();
        });
    }
    if (summaryFilterCategory) {
        summaryFilterCategory.addEventListener("change", () => {
            renderPerfSummaryTable();
        });
    }
    if (summaryFilterStatus) {
        summaryFilterStatus.addEventListener("change", () => {
            renderPerfSummaryTable();
        });
    }

    const topCTVSortSelect = document.getElementById("topCTVSortSelect");
    if (topCTVSortSelect) {
        topCTVSortSelect.addEventListener("change", () => {
            renderTopCTVTable();
        });
    }

    const topCTVBestSort1 = document.getElementById("topCTVBestSort1");
    const topCTVBestSort2 = document.getElementById("topCTVBestSort2");
    if (topCTVBestSort1) {
        topCTVBestSort1.addEventListener("change", () => {
            renderTopCTVBestTable();
        });
    }
    if (topCTVBestSort2) {
        topCTVBestSort2.addEventListener("change", () => {
            renderTopCTVBestTable();
        });
    }

    const perfF1GroupFilter = document.getElementById("perfF1GroupFilter");
    if (perfF1GroupFilter) {
        perfF1GroupFilter.addEventListener("change", () => {
            renderF1CategoryTable();
        });
    }

    const perfF1UserSearch = document.getElementById("perfF1UserSearch");
    if (perfF1UserSearch) {
        perfF1UserSearch.addEventListener("input", () => {
            renderF1CategoryTable();
        });
    }

    const perfF1CategoryStartDate = document.getElementById("perfF1CategoryStartDate");
    const perfF1CategoryEndDate = document.getElementById("perfF1CategoryEndDate");
    const perfF1CategoryFilterDate = document.getElementById("perfF1CategoryFilterDate");

    if (perfF1CategoryStartDate) {
        perfF1CategoryStartDate.addEventListener("change", renderF1CategoryTable);
    }
    if (perfF1CategoryEndDate) {
        perfF1CategoryEndDate.addEventListener("change", renderF1CategoryTable);
    }
    if (perfF1CategoryFilterDate) {
        perfF1CategoryFilterDate.addEventListener("input", renderF1CategoryTable);
    }

    const tableHeaders = document.querySelectorAll("th[data-perf-sort]");
    tableHeaders.forEach(th => {
        th.addEventListener("click", () => {
            const column = th.getAttribute("data-perf-sort");
            if (currentPerfSortColumn === column) {
                currentPerfSortDirection = currentPerfSortDirection === "asc" ? "desc" : "asc";
            } else {
                currentPerfSortColumn = column;
                currentPerfSortDirection = "asc";
            }
            
            tableHeaders.forEach(header => {
                header.classList.remove("sort-asc", "sort-desc");
            });
            th.classList.add(currentPerfSortDirection === "asc" ? "sort-asc" : "sort-desc");
            
            sortFilteredPerfData();
            renderPerfTable();
        });
    });

    const btnExportTopCTVWorst = document.getElementById("btnExportTopCTVWorst");
    if (btnExportTopCTVWorst) {
        btnExportTopCTVWorst.addEventListener("click", () => {
            const todayStr = new Date().toISOString().split("T")[0];
            downloadTableToExcel("topCTVWorstTable", `BaoCao_Top10_CTV_Lech_${todayStr}.csv`);
        });
    }

    const btnExportTopCTVBest = document.getElementById("btnExportTopCTVBest");
    if (btnExportTopCTVBest) {
        btnExportTopCTVBest.addEventListener("click", () => {
            const todayStr = new Date().toISOString().split("T")[0];
            downloadTableToExcel("topCTVBestTable", `BaoCao_Top10_CTV_TotNhat_${todayStr}.csv`);
        });
    }

    const btnExportSummary = document.getElementById("btnExportSummary");
    if (btnExportSummary) {
        btnExportSummary.addEventListener("click", () => {
            const todayStr = new Date().toISOString().split("T")[0];
            downloadTableToExcel("perfSummaryTable", `BaoCao_TomTatHieuSuat_${todayStr}.csv`);
        });
    }
}

// Bind Category tab filters event listeners
function setupCategoryEventListeners(earliestDate, latestDate) {
    setupMultiSelectDropdown("catFilterGroupContainer");
    
    const catStartDate = document.getElementById("catFilterStartDate");
    const catEndDate = document.getElementById("catFilterEndDate");
    const vegLevel3FilterDate = document.getElementById("vegLevel3FilterDate");
    const vegLevel3DateFilterDate = document.getElementById("vegLevel3DateFilterDate");
    if (catStartDate) catStartDate.addEventListener("change", renderF1CategoryTable);
    if (catEndDate) catEndDate.addEventListener("change", renderF1CategoryTable);
    if (vegLevel3FilterDate) {
        vegLevel3FilterDate.addEventListener("input", () => {
            renderVegetablesLevel3Table();
        });
    }
    if (vegLevel3DateFilterDate) {
        vegLevel3DateFilterDate.addEventListener("input", () => {
            renderVegetablesLevel3DateTable();
        });
    }

    // Bind table-specific date filter listeners
    const bindDateFilters = (startId, endId, renderFunc) => {
        const startEl = document.getElementById(startId);
        const endEl = document.getElementById(endId);
        if (startEl) startEl.addEventListener("change", renderFunc);
        if (endEl) endEl.addEventListener("change", renderFunc);
    };

    bindDateFilters("catDateTableStartDate", "catDateTableEndDate", renderF1CategoryDateTable);
    bindDateFilters("topSkuStartDate", "topSkuEndDate", renderTopSkuDiscrepancyTable);
    bindDateFilters("vegLevel3DateStartDate", "vegLevel3DateEndDate", renderVegetablesLevel3DateTable);
    bindDateFilters("vegLevel3StartDate", "vegLevel3EndDate", renderVegetablesLevel3Table);
    
    const catClearFiltersBtn = document.getElementById("catClearFiltersBtn");
    if (catClearFiltersBtn) {
        catClearFiltersBtn.addEventListener("click", () => {
            if (catStartDate) catStartDate.value = earliestDate;
            if (catEndDate) catEndDate.value = latestDate;
            if (vegLevel3FilterDate) vegLevel3FilterDate.value = "";
            if (vegLevel3DateFilterDate) vegLevel3DateFilterDate.value = "";

            // Clear table-specific date filters
            const clearInputs = ["catDateTableStartDate", "catDateTableEndDate", "topSkuStartDate", "topSkuEndDate", "vegLevel3DateStartDate", "vegLevel3DateEndDate", "vegLevel3StartDate", "vegLevel3EndDate"];
            clearInputs.forEach(id => {
                const el = document.getElementById(id);
                if (el) el.value = "";
            });
            
            const groupContainer = document.getElementById("catFilterGroupContainer");
            if (groupContainer) {
                groupContainer.querySelectorAll("input[type='checkbox']").forEach(cb => cb.checked = true);
                updateSelectLabel(groupContainer, groupContainer.querySelector(".multiselect-value"));
            }
            
            const searchInput = document.getElementById("perfF1UserSearch");
            if (searchInput) searchInput.value = "";
            
            const selectFilter = document.getElementById("perfF1GroupFilter");
            if (selectFilter) selectFilter.value = "All";

            const topSkuCategoryFilter = document.getElementById("topSkuCategoryFilter");
            if (topSkuCategoryFilter) topSkuCategoryFilter.value = "All";

            const topSkuSearchInput = document.getElementById("topSkuSearchInput");
            if (topSkuSearchInput) topSkuSearchInput.value = "";

            const topSkuSortCriteria = document.getElementById("topSkuSortCriteria");
            if (topSkuSortCriteria) topSkuSortCriteria.value = "qty";
            
            renderF1CategoryTable();
        });
    }

    const catDateTableFilterDate = document.getElementById("catDateTableFilterDate");
    if (catDateTableFilterDate) {
        catDateTableFilterDate.addEventListener("input", () => {
            renderF1CategoryDateTable();
        });
    }

    const perfCatDateBtnExport = document.getElementById("perfCatDateBtnExport");
    if (perfCatDateBtnExport) {
        perfCatDateBtnExport.addEventListener("click", () => {
            downloadCategoryDateTabular();
        });
    }

    const perfCatF1BtnExport = document.getElementById("perfCatF1BtnExport");
    if (perfCatF1BtnExport) {
        perfCatF1BtnExport.addEventListener("click", () => {
            downloadCategoryF1Tabular();
        });
    }

    const perfVegLevel3DateBtnExport = document.getElementById("perfVegLevel3DateBtnExport");
    if (perfVegLevel3DateBtnExport) {
        const newBtn = perfVegLevel3DateBtnExport.cloneNode(true);
        perfVegLevel3DateBtnExport.parentNode.replaceChild(newBtn, perfVegLevel3DateBtnExport);
        newBtn.addEventListener("click", () => {
            const todayStr = new Date().toISOString().split("T")[0];
            downloadTableToExcel("perfVegLevel3DateTable", `BaoCao_HieuSuatRauCu_Level3_TheoNgay_${todayStr}.csv`);
        });
    }

    const topSkuCategoryFilter = document.getElementById("topSkuCategoryFilter");
    if (topSkuCategoryFilter) {
        topSkuCategoryFilter.addEventListener("change", () => {
            renderTopSkuDiscrepancyTable();
        });
    }

    const topSkuSortCriteria = document.getElementById("topSkuSortCriteria");
    if (topSkuSortCriteria) {
        topSkuSortCriteria.addEventListener("change", () => {
            renderTopSkuDiscrepancyTable();
        });
    }

    const topSkuSearchInput = document.getElementById("topSkuSearchInput");
    if (topSkuSearchInput) {
        topSkuSearchInput.addEventListener("input", () => {
            renderTopSkuDiscrepancyTable();
        });
    }

    const topSkuBtnExport = document.getElementById("topSkuBtnExport");
    if (topSkuBtnExport) {
        const newBtn = topSkuBtnExport.cloneNode(true);
        topSkuBtnExport.parentNode.replaceChild(newBtn, topSkuBtnExport);
        newBtn.addEventListener("click", () => {
            const todayStr = new Date().toISOString().split("T")[0];
            downloadTableToExcel("topSkuDiscrepancyTable", `BaoCao_Top10_SKU_Lech_${todayStr}.csv`);
        });
    }
}

// Bind Tabular Export tab events
function setupExportTabEventListeners(earliestDate, latestDate) {
    const exportDatasetSelect = document.getElementById("exportDatasetSelect");
    const exportStartDate = document.getElementById("exportStartDate");
    const exportEndDate = document.getElementById("exportEndDate");
    const btnExportTabular = document.getElementById("btnExportTabular");

    if (exportDatasetSelect) exportDatasetSelect.addEventListener("change", renderExportPreview);
    if (exportStartDate) exportStartDate.addEventListener("change", renderExportPreview);
    if (exportEndDate) exportEndDate.addEventListener("change", renderExportPreview);
    if (btnExportTabular) btnExportTabular.addEventListener("click", downloadExportDataset);
}

// Autocomplete render and checkbox logic for Performance Search
function onPerfItemSearchInput(e) {
    const searchVal = e.target.value.toLowerCase().trim();
    const listContainer = document.getElementById("perfItemDropdownList");
    
    if (searchVal === "") {
        hidePerfItemDropdownList();
        return;
    }

    const searchValClean = removeVietnameseTones(searchVal);
    const searchValCleanY = searchValClean.replace(/y/g, 'i');
    const matchedCodes = Object.keys(masterItems).filter(code => {
        const nameClean = removeVietnameseTones(masterItems[code].name.toLowerCase());
        const nameCleanY = nameClean.replace(/y/g, 'i');
        return code.toLowerCase().includes(searchVal) || 
               nameClean.includes(searchValClean) || 
               nameCleanY.includes(searchValCleanY);
    }).slice(0, 30);

    if (matchedCodes.length === 0) {
        hidePerfItemDropdownList();
        return;
    }

    listContainer.innerHTML = "";
    
    if (matchedCodes.length > 1) {
        const selectAllDiv = document.createElement("div");
        selectAllDiv.className = "dropdown-search-item";
        selectAllDiv.style.borderBottom = "1px solid var(--border-color)";
        selectAllDiv.style.fontWeight = "600";
        selectAllDiv.style.display = "flex";
        selectAllDiv.style.alignItems = "center";
        
        selectAllDiv.innerHTML = `
            <input type="checkbox" id="perfSuggestionSelectAll" style="margin-right: 8px; cursor: pointer; accent-color: var(--color-primary);">
            <label for="perfSuggestionSelectAll" style="cursor: pointer; display: flex; align-items: center; width: 100%;">Chọn tất cả kết quả gợi ý</label>
        `;
        listContainer.appendChild(selectAllDiv);
        
        const selectAllCb = selectAllDiv.querySelector("#perfSuggestionSelectAll");
        selectAllCb.addEventListener("change", (e) => {
            const isChecked = e.target.checked;
            listContainer.querySelectorAll(".perf-suggestion-checkbox").forEach(cb => {
                cb.checked = isChecked;
            });
        });
    }

    matchedCodes.forEach(code => {
        const div = document.createElement("div");
        div.className = "dropdown-search-item";
        div.style.display = "flex";
        div.style.alignItems = "center";
        
        const isChecked = selectedPerfItemCodes.includes(code) ? "checked" : "";
        
        div.innerHTML = `
            <input type="checkbox" class="perf-suggestion-checkbox" data-code="${code}" ${isChecked} style="margin-right: 8px; cursor: pointer; accent-color: var(--color-primary);">
            <span style="cursor: pointer; flex: 1;">${code} - ${masterItems[code].name}</span>
        `;
        
        div.addEventListener("click", (ev) => {
            if (ev.target.type !== "checkbox") {
                const cb = div.querySelector(".perf-suggestion-checkbox");
                cb.checked = !cb.checked;
            }
            updatePerfSelectAllCheckboxState(listContainer);
        });
        
        listContainer.appendChild(div);
    });

    const actionDiv = document.createElement("div");
    actionDiv.style.padding = "8px 12px";
    actionDiv.style.borderTop = "1px solid var(--border-color)";
    actionDiv.style.display = "flex";
    actionDiv.style.justifyContent = "space-between";
    actionDiv.style.alignItems = "center";
    actionDiv.style.backgroundColor = "var(--bg-secondary)";
    
    actionDiv.innerHTML = `
        <span style="font-size: 11px; color: var(--text-muted);">Nhấn Enter hoặc click nút</span>
        <button type="button" class="btn btn-primary" id="btnConfirmPerfSuggestions" style="padding: 4px 10px; font-size: 12px; height: auto; line-height: 1;">Xác nhận chọn</button>
    `;
    
    actionDiv.addEventListener("click", (ev) => {
        ev.stopPropagation();
    });
    
    listContainer.appendChild(actionDiv);
    
    actionDiv.querySelector("#btnConfirmPerfSuggestions").addEventListener("click", () => {
        confirmSelectedPerfSuggestions();
    });

    updatePerfSelectAllCheckboxState(listContainer);
    listContainer.style.display = "block";
}

function updatePerfSelectAllCheckboxState(listContainer) {
    const selectAllCb = listContainer.querySelector("#perfSuggestionSelectAll");
    if (!selectAllCb) return;
    
    const checkboxes = Array.from(listContainer.querySelectorAll(".perf-suggestion-checkbox"));
    const checkedCount = checkboxes.filter(cb => cb.checked).length;
    
    if (checkedCount === 0) {
        selectAllCb.checked = false;
        selectAllCb.indeterminate = false;
    } else if (checkedCount === checkboxes.length) {
        selectAllCb.checked = true;
        selectAllCb.indeterminate = false;
    } else {
        selectAllCb.checked = false;
        selectAllCb.indeterminate = true;
    }
}

function confirmSelectedPerfSuggestions() {
    const listContainer = document.getElementById("perfItemDropdownList");
    const checkboxes = listContainer.querySelectorAll(".perf-suggestion-checkbox");
    const input = document.getElementById("perfFilterItemCode");
    
    if (checkboxes.length === 0) {
        const searchVal = input.value.toLowerCase().trim();
        if (searchVal !== "") {
            const searchValClean = removeVietnameseTones(searchVal);
            const searchValCleanY = searchValClean.replace(/y/g, 'i');
            const matchedCodes = Object.keys(masterItems).filter(code => {
                const nameClean = removeVietnameseTones(masterItems[code].name.toLowerCase());
                const nameCleanY = nameClean.replace(/y/g, 'i');
                return code.toLowerCase().includes(searchVal) || 
                       nameClean.includes(searchValClean) || 
                       nameCleanY.includes(searchValCleanY);
            });
            if (matchedCodes.length > 0) {
                matchedCodes.forEach(code => {
                    if (!selectedPerfItemCodes.includes(code)) {
                        selectedPerfItemCodes.push(code);
                    }
                });
                renderPerfItemTags();
                applyPerfFiltersAndRender();
                showToast(`Đã chọn nhanh các sản phẩm chứa từ khóa "${input.value}"`);
            }
        }
        input.value = "";
        hidePerfItemDropdownList();
        return;
    }

    let changed = false;
    const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
    checkboxes.forEach(cb => {
        const code = cb.getAttribute("data-code");
        const shouldBeChecked = anyChecked ? cb.checked : true;
        if (shouldBeChecked) {
            if (!selectedPerfItemCodes.includes(code)) {
                selectedPerfItemCodes.push(code);
                changed = true;
            }
        } else {
            if (selectedPerfItemCodes.includes(code)) {
                selectedPerfItemCodes = selectedPerfItemCodes.filter(c => c !== code);
                changed = true;
            }
        }
    });

    if (changed) {
        renderPerfItemTags();
        applyPerfFiltersAndRender();
        showToast("Đã cập nhật lựa chọn sản phẩm");
    }
    
    input.value = "";
    hidePerfItemDropdownList();
}

function renderPerfItemTags() {
    const container = document.getElementById("perfItemTagsContainer");
    const input = document.getElementById("perfFilterItemCode");
    
    if (!container || !input) return;
    
    container.innerHTML = "";
    selectedPerfItemCodes.forEach(code => {
        const tag = document.createElement("span");
        tag.className = "tag";
        tag.innerHTML = `
            ${code}
            <span class="perf-tag-close" data-code="${code}">&times;</span>
        `;
        container.appendChild(tag);
    });
    
    container.appendChild(input);
    input.focus();
    
    container.querySelectorAll(".perf-tag-close").forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const codeToRemove = btn.getAttribute("data-code");
            selectedPerfItemCodes = selectedPerfItemCodes.filter(c => c !== codeToRemove);
            renderPerfItemTags();
            applyPerfFiltersAndRender();
        });
    });
}

function hidePerfItemDropdownList() {
    const el = document.getElementById("perfItemDropdownList");
    if (el) el.style.display = "none";
}

// Autocomplete render and checkbox logic for Summary Product Search
function onSummaryProductSearchInput(e) {
    const searchVal = e.target.value.toLowerCase().trim();
    const listContainer = document.getElementById("perfSummaryItemDropdownList");

    if (searchVal === "") {
        hideSummaryProductDropdownList();
        return;
    }

    const searchValClean = removeVietnameseTones(searchVal);
    const searchValCleanY = searchValClean.replace(/y/g, 'i');
    const matchedCodes = Object.keys(masterItems).filter(code => {
        const nameClean = removeVietnameseTones(masterItems[code].name.toLowerCase());
        const nameCleanY = nameClean.replace(/y/g, 'i');
        return code.toLowerCase().includes(searchVal) || 
               nameClean.includes(searchValClean) || 
               nameCleanY.includes(searchValCleanY);
    }).slice(0, 30);

    if (matchedCodes.length === 0) {
        hideSummaryProductDropdownList();
        return;
    }

    listContainer.innerHTML = "";

    if (matchedCodes.length > 1) {
        const selectAllDiv = document.createElement("div");
        selectAllDiv.className = "dropdown-search-item";
        selectAllDiv.style.borderBottom = "1px solid var(--border-color)";
        selectAllDiv.style.fontWeight = "600";
        selectAllDiv.style.display = "flex";
        selectAllDiv.style.alignItems = "center";

        selectAllDiv.innerHTML = `
            <input type="checkbox" id="summaryProductSuggestionSelectAll" style="margin-right: 8px; cursor: pointer; accent-color: var(--color-primary);">
            <label for="summaryProductSuggestionSelectAll" style="cursor: pointer; display: flex; align-items: center; width: 100%;">Chọn tất cả kết quả gợi ý</label>
        `;
        listContainer.appendChild(selectAllDiv);

        const selectAllCb = selectAllDiv.querySelector("#summaryProductSuggestionSelectAll");
        selectAllCb.addEventListener("change", (e) => {
            const isChecked = e.target.checked;
            listContainer.querySelectorAll(".summary-product-suggestion-checkbox").forEach(cb => {
                cb.checked = isChecked;
            });
        });
    }

    matchedCodes.forEach(code => {
        const div = document.createElement("div");
        div.className = "dropdown-search-item";
        div.style.display = "flex";
        div.style.alignItems = "center";

        const isChecked = selectedSummaryProductCodes.includes(code) ? "checked" : "";

        div.innerHTML = `
            <input type="checkbox" class="summary-product-suggestion-checkbox" data-code="${code}" ${isChecked} style="margin-right: 8px; cursor: pointer; accent-color: var(--color-primary);">
            <span style="cursor: pointer; flex: 1;">${code} - ${masterItems[code].name}</span>
        `;

        div.addEventListener("click", (ev) => {
            if (ev.target.type !== "checkbox") {
                const cb = div.querySelector(".summary-product-suggestion-checkbox");
                cb.checked = !cb.checked;
            }
            updateSummaryProductSelectAllCheckboxState(listContainer);
        });

        listContainer.appendChild(div);
    });

    const actionDiv = document.createElement("div");
    actionDiv.style.padding = "8px 12px";
    actionDiv.style.borderTop = "1px solid var(--border-color)";
    actionDiv.style.display = "flex";
    actionDiv.style.justifyContent = "space-between";
    actionDiv.style.alignItems = "center";
    actionDiv.style.backgroundColor = "var(--bg-secondary)";

    actionDiv.innerHTML = `
        <span style="font-size: 11px; color: var(--text-muted);">Nhấn Enter hoặc click nút</span>
        <button type="button" class="btn btn-primary" id="btnConfirmSummaryProductSuggestions" style="padding: 4px 10px; font-size: 12px; height: auto; line-height: 1;">Xác nhận chọn</button>
    `;

    actionDiv.addEventListener("click", (ev) => {
        ev.stopPropagation();
    });

    listContainer.appendChild(actionDiv);

    actionDiv.querySelector("#btnConfirmSummaryProductSuggestions").addEventListener("click", () => {
        confirmSelectedSummaryProductSuggestions();
    });

    updateSummaryProductSelectAllCheckboxState(listContainer);
    listContainer.style.display = "block";
}

function updateSummaryProductSelectAllCheckboxState(listContainer) {
    const selectAllCb = listContainer.querySelector("#summaryProductSuggestionSelectAll");
    if (!selectAllCb) return;

    const checkboxes = Array.from(listContainer.querySelectorAll(".summary-product-suggestion-checkbox"));
    const checkedCount = checkboxes.filter(cb => cb.checked).length;

    if (checkedCount === 0) {
        selectAllCb.checked = false;
        selectAllCb.indeterminate = false;
    } else if (checkedCount === checkboxes.length) {
        selectAllCb.checked = true;
        selectAllCb.indeterminate = false;
    } else {
        selectAllCb.checked = false;
        selectAllCb.indeterminate = true;
    }
}

function confirmSelectedSummaryProductSuggestions() {
    const listContainer = document.getElementById("perfSummaryItemDropdownList");
    const checkboxes = listContainer.querySelectorAll(".summary-product-suggestion-checkbox");
    const input = document.getElementById("perfSummaryFilterProduct");

    if (checkboxes.length === 0) {
        const searchVal = input.value.toLowerCase().trim();
        if (searchVal !== "") {
            const searchValClean = removeVietnameseTones(searchVal);
            const searchValCleanY = searchValClean.replace(/y/g, 'i');
            const matchedCodes = Object.keys(masterItems).filter(code => {
                const nameClean = removeVietnameseTones(masterItems[code].name.toLowerCase());
                const nameCleanY = nameClean.replace(/y/g, 'i');
                return code.toLowerCase().includes(searchVal) || 
                       nameClean.includes(searchValClean) || 
                       nameCleanY.includes(searchValCleanY);
            });
            if (matchedCodes.length > 0) {
                matchedCodes.forEach(code => {
                    if (!selectedSummaryProductCodes.includes(code)) {
                        selectedSummaryProductCodes.push(code);
                    }
                });
                renderSummaryProductTags();
                renderPerfSummaryTable();
                showToast(`Đã chọn nhanh các sản phẩm chứa từ khóa "${input.value}"`);
            }
        }
        input.value = "";
        hideSummaryProductDropdownList();
        return;
    }

    let changed = false;
    const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
    checkboxes.forEach(cb => {
        const code = cb.getAttribute("data-code");
        const shouldBeChecked = anyChecked ? cb.checked : true;
        if (shouldBeChecked) {
            if (!selectedSummaryProductCodes.includes(code)) {
                selectedSummaryProductCodes.push(code);
                changed = true;
            }
        } else {
            if (selectedSummaryProductCodes.includes(code)) {
                selectedSummaryProductCodes = selectedSummaryProductCodes.filter(c => c !== code);
                changed = true;
            }
        }
    });

    if (changed) {
        renderSummaryProductTags();
        renderPerfSummaryTable();
        showToast("Đã cập nhật lựa chọn sản phẩm");
    }

    input.value = "";
    hideSummaryProductDropdownList();
}

function renderSummaryProductTags() {
    const container = document.getElementById("perfSummaryItemTagsContainer");
    const input = document.getElementById("perfSummaryFilterProduct");

    if (!container || !input) return;

    // Save current input value
    const currentInputValue = input.value;

    container.innerHTML = "";
    selectedSummaryProductCodes.forEach(code => {
        const tag = document.createElement("span");
        tag.className = "tag";
        tag.style.padding = "2px 6px";
        tag.style.fontSize = "11px";
        tag.style.borderRadius = "var(--radius-sm)";
        tag.innerHTML = `
            ${code}
            <span class="summary-product-tag-close" data-code="${code}" style="cursor: pointer; margin-left: 4px; font-weight: bold;">&times;</span>
        `;
        container.appendChild(tag);
    });

    input.placeholder = selectedSummaryProductCodes.length > 0 ? "" : "Chọn nhiều sản phẩm...";
    container.appendChild(input);
    input.value = currentInputValue;
    input.focus();

    container.querySelectorAll(".summary-product-tag-close").forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const codeToRemove = btn.getAttribute("data-code");
            selectedSummaryProductCodes = selectedSummaryProductCodes.filter(c => c !== codeToRemove);
            renderSummaryProductTags();
            renderPerfSummaryTable();
        });
    });
}

function hideSummaryProductDropdownList() {
    const el = document.getElementById("perfSummaryItemDropdownList");
    if (el) el.style.display = "none";
}

// Clear all Performance report filters
function clearPerfFilters() {
    selectedPerfItemCodes = [];
    renderPerfItemTags();

    selectedSummaryProductCodes = [];
    renderSummaryProductTags();

    document.getElementById("perfFilterItemCode").value = "";
    document.getElementById("perfFilterStartDate").value = "";
    document.getElementById("perfFilterEndDate").value = "";

    const summaryFilterDate = document.getElementById("perfSummaryFilterDate");
    const summaryFilterUser = document.getElementById("perfSummaryFilterUser");
    const summaryFilterProduct = document.getElementById("perfSummaryFilterProduct");
    const summaryFilterCategory = document.getElementById("perfSummaryFilterCategory");
    const summaryFilterStatus = document.getElementById("perfSummaryFilterStatus");
    if (summaryFilterDate) summaryFilterDate.value = "";
    if (summaryFilterUser) summaryFilterUser.value = "";
    if (summaryFilterProduct) summaryFilterProduct.value = "";
    if (summaryFilterCategory) summaryFilterCategory.value = "";
    if (summaryFilterStatus) summaryFilterStatus.value = "";
    
    const tableFilterDate = document.getElementById("perfTableFilterDate");
    const tableFilterUser = document.getElementById("perfTableFilterUser");
    const tableFilterBarcode = document.getElementById("perfTableFilterBarcode");
    const tableFilterName = document.getElementById("perfTableFilterName");
    const tableFilterUnit = document.getElementById("perfTableFilterUnit");
    if (tableFilterDate) tableFilterDate.value = "";
    if (tableFilterUser) tableFilterUser.value = "";
    if (tableFilterBarcode) tableFilterBarcode.value = "";
    if (tableFilterName) tableFilterName.value = "";
    if (tableFilterUnit) tableFilterUnit.value = "";
    
    const perfF1UserSearch = document.getElementById("perfF1UserSearch");
    if (perfF1UserSearch) perfF1UserSearch.value = "";
    
    const perfF1CategoryStartDate = document.getElementById("perfF1CategoryStartDate");
    const perfF1CategoryEndDate = document.getElementById("perfF1CategoryEndDate");
    const perfF1CategoryFilterDate = document.getElementById("perfF1CategoryFilterDate");
    if (perfF1CategoryStartDate) perfF1CategoryStartDate.value = "";
    if (perfF1CategoryEndDate) perfF1CategoryEndDate.value = "";
    if (perfF1CategoryFilterDate) perfF1CategoryFilterDate.value = "";
    
    document.querySelectorAll("#perfFilterStatusContainer input[type='checkbox']").forEach(cb => cb.checked = false);
    updateSelectLabel(document.getElementById("perfFilterStatusContainer"), document.querySelector("#perfFilterStatusContainer .multiselect-value"));
    
    document.querySelectorAll("#perfFilterGroupContainer input[type='checkbox']").forEach(cb => cb.checked = false);
    updateSelectLabel(document.getElementById("perfFilterGroupContainer"), document.querySelector("#perfFilterGroupContainer .multiselect-value"));
    
    document.querySelectorAll("#perfFilterUserContainer input[type='checkbox']").forEach(cb => cb.checked = false);
    updateSelectLabel(document.getElementById("perfFilterUserContainer"), document.querySelector("#perfFilterUserContainer .multiselect-value"));
    
    document.querySelectorAll("#perfFilterToBranchContainer input[type='checkbox']").forEach(cb => cb.checked = false);
    updateSelectLabel(document.getElementById("perfFilterToBranchContainer"), document.querySelector("#perfFilterToBranchContainer .multiselect-value"));
    
    // Reset unit filter checkboxes
    const perfFilterUnitContainer = document.getElementById("perfFilterUnitContainer");
    if (perfFilterUnitContainer) {
        perfFilterUnitContainer.querySelectorAll("input[type='checkbox']").forEach(cb => cb.checked = false);
        updateSelectLabel(perfFilterUnitContainer, perfFilterUnitContainer.querySelector(".multiselect-value"));
    }

    // Reset category filter checkboxes
    const perfFilterCategoryContainer = document.getElementById("perfFilterCategoryContainer");
    if (perfFilterCategoryContainer) {
        perfFilterCategoryContainer.querySelectorAll("input[type='checkbox']").forEach(cb => cb.checked = false);
        updateSelectLabel(perfFilterCategoryContainer, perfFilterCategoryContainer.querySelector(".multiselect-value"));
    }
    
    hidePerfItemDropdownList();
    hideSummaryProductDropdownList();
    applyPerfFiltersAndRender();
}

// Helper to determine performance row status, checking for kg hao hut
function getPerfStatus(t) {
    const statusInfo = calculateStatus(t);
    return statusInfo.statusText;
}

// Apply filter conditions for Performance dataset and re-render
function applyPerfFiltersAndRender() {
    const startDateQuery = document.getElementById("perfFilterStartDate") ? document.getElementById("perfFilterStartDate").value : "";
    const endDateQuery = document.getElementById("perfFilterEndDate") ? document.getElementById("perfFilterEndDate").value : "";

    const selectedUsers = Array.from(document.querySelectorAll("#perfFilterUserContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedStatuses = Array.from(document.querySelectorAll("#perfFilterStatusContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedToBranches = Array.from(document.querySelectorAll("#perfFilterToBranchContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedUnits = Array.from(document.querySelectorAll("#perfFilterUnitContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedPerfCategories = Array.from(document.querySelectorAll("#perfFilterCategoryContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedGroups = Array.from(document.querySelectorAll("#perfFilterGroupContainer input[type='checkbox']:checked")).map(cb => cb.value);

    const inputEl = document.getElementById("perfFilterItemCode");
    const textQuery = inputEl ? inputEl.value.toLowerCase().trim() : "";

    filteredPerfTransfers = transfers.filter(t => {
        // Only evaluate main KHO RAU CỦ transfers for CTV performance reports
        if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") {
            return false;
        }
        // Keep only F1, F2, HUYHOANG, CTV, and exclude empty/unknown dividing staff
        if (!t.nguoiChia) {
            return false;
        }
        const name = t.nguoiChia.trim().toLowerCase().normalize("NFC");
        const excluded = ["nhan quang hiếu", "nhân quang hiếu", "nhan quang hieu", "nhân quang hieu"];
        if (name === "" || excluded.includes(name)) {
            return false;
        }

        // Match staff group
        let matchGroup = true;
        if (selectedGroups.length > 0) {
            matchGroup = false;
            for (const g of selectedGroups) {
                if (name.startsWith(g.toLowerCase())) {
                    matchGroup = true;
                    break;
                }
            }
        }
        if (!matchGroup) return false;

        const statusInfo = calculateStatus(t);
        const status = statusInfo.statusText; // Thiếu, Dư, Hao hụt, Đủ, Đang chuyển

        // Match item
        const matchItem = (selectedPerfItemCodes.length === 0 && textQuery === "") || 
            selectedPerfItemCodes.includes(t.itemCode) ||
            (textQuery !== "" && (t.itemCode.toLowerCase() === textQuery || t.itemName.toLowerCase() === textQuery));
        
        // Match user
        const matchUser = selectedUsers.length === 0 || selectedUsers.includes(t.nguoiChia);
        
        // Match status
        const perfStatus = status;
        const matchStatus = selectedStatuses.length === 0 || selectedStatuses.includes(perfStatus);
        
        // Match to branch (Nơi nhận)
        const matchToBranch = selectedToBranches.length === 0 || selectedToBranches.includes(t.toBranch);
        
        // Match unit
        const matchUnit = selectedUnits.length === 0 || selectedUnits.includes(t.unit);
        
        // Match dates
        const matchStartDate = startDateQuery === "" || t.date >= startDateQuery;
        const matchEndDate = endDateQuery === "" || t.date <= endDateQuery;
        
        // Match category
        const matchCategory = selectedPerfCategories.length === 0 || selectedPerfCategories.includes(t.nganhHang);

        return matchItem && matchUser && matchStatus && matchToBranch && matchStartDate && matchEndDate && matchUnit && matchCategory;
    });

    currentPerfPage = 1;
    sortFilteredPerfData();
    renderPerfTable();
    updatePerfSummary();
    renderTopCTVTable();
    renderTopCTVBestTable();
    renderPerfSummaryTable();
    renderF1CategoryTable();
}

// Render summary of Top 10 CTVs with highest discrepant counts
function renderTopCTVTable() {
    const tbody = document.getElementById("perfTopCTVBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    // Extract performance active filter criteria
    const startDateQuery = document.getElementById("perfFilterStartDate") ? document.getElementById("perfFilterStartDate").value : "";
    const endDateQuery = document.getElementById("perfFilterEndDate") ? document.getElementById("perfFilterEndDate").value : "";
    const selectedUsers = Array.from(document.querySelectorAll("#perfFilterUserContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedToBranches = Array.from(document.querySelectorAll("#perfFilterToBranchContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedUnits = Array.from(document.querySelectorAll("#perfFilterUnitContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedGroups = Array.from(document.querySelectorAll("#perfFilterGroupContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const inputEl = document.getElementById("perfFilterItemCode");
    const textQuery = inputEl ? inputEl.value.toLowerCase().trim() : "";

    // Filter the shipping transfers (Tab 1 dataset) based on Tab 2 performance filters
    const activeTransfers = transfers.filter(t => {
        // Only evaluate main KHO RAU CỦ transfers for CTV performance reports
        if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") {
            return false;
        }
        // Keep only F1, F2, HUYHOANG, CTV, and exclude empty/unknown dividing staff
        if (!t.nguoiChia) {
            return false;
        }
        const name = t.nguoiChia.trim().toLowerCase();
        if (!(name.startsWith("f1") || name.startsWith("f2") || name.startsWith("huyhoang") || name.startsWith("ctv"))) {
            return false;
        }

        // Match staff group
        let matchGroup = true;
        if (selectedGroups.length > 0) {
            matchGroup = false;
            for (const g of selectedGroups) {
                if (name.startsWith(g.toLowerCase())) {
                    matchGroup = true;
                    break;
                }
            }
        }
        if (!matchGroup) return false;

        // Match items
        const matchItem = (selectedPerfItemCodes.length === 0 && textQuery === "") || 
            selectedPerfItemCodes.includes(t.itemCode) ||
            (textQuery !== "" && (t.itemCode.toLowerCase() === textQuery || t.itemName.toLowerCase() === textQuery));
        
        // Match user
        const matchUser = selectedUsers.length === 0 || selectedUsers.includes(t.nguoiChia);
        
        // Match to branch (Nơi nhận)
        const matchToBranch = selectedToBranches.length === 0 || selectedToBranches.includes(t.toBranch);
        
        // Match unit
        const matchUnit = selectedUnits.length === 0 || selectedUnits.includes(t.unit);
        
        // Match dates
        const matchStartDate = startDateQuery === "" || t.date >= startDateQuery;
        const matchEndDate = endDateQuery === "" || t.date <= endDateQuery;

        return matchItem && matchUser && matchToBranch && matchStartDate && matchEndDate && matchUnit;
    });

    // Aggregate discrepancy data by nguoiChia
    const userAgg = {};
    activeTransfers.forEach(t => {
        const user = t.nguoiChia || "Không rõ";
        if (!userAgg[user]) {
            userAgg[user] = {
                user: user,
                dates: new Set(),
                storesShared: new Set(),
                storesDiscrepant: new Set(),
                totalLines: 0,
                discrepantLines: 0,
                diffQtyKg: 0,
                diffQtyPack: 0,
                totalReqQty: 0,
                totalDiffQty: 0,
                totalSharedQty: 0
            };
        }
        if (t.date) {
            userAgg[user].dates.add(t.date);
        }

        const statusInfo = calculateStatus(t);
        
        // Skip in-transit rows from total lines, req qty and error calculations
        if (statusInfo.statusText === "Đang chuyển") {
            return;
        }

        const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");

        if (t.toBranch) {
            const branchName = t.toBranch.trim();
            userAgg[user].storesShared.add(branchName);
            if (isDiscrepant) {
                userAgg[user].storesDiscrepant.add(branchName);
            }
        }

        userAgg[user].totalLines += 1;
        userAgg[user].totalReqQty += t.qtyShipped;
        userAgg[user].totalSharedQty += (t.qtyReceived + (t.matchedCorrectiveQty || 0));

        if (isDiscrepant) {
            userAgg[user].discrepantLines += 1;
            const absDiff = Math.abs(statusInfo.chenhLechConLai);
            userAgg[user].totalDiffQty += absDiff;
            
            const isKg = (t.unit && t.unit.toLowerCase() === "kg");
            if (isKg) {
                userAgg[user].diffQtyKg += absDiff;
            } else {
                userAgg[user].diffQtyPack += absDiff;
            }
        }
    });

    const sortSelect = document.getElementById("topCTVSortSelect");
    const sortVal = sortSelect ? sortSelect.value : "stErrorRate";

    // Static title text update
    const titleTextEl = document.getElementById("topCTVTitleText");
    if (titleTextEl) {
        titleTextEl.innerText = "Top 10 CTV chia sai lệch nhiều nhất";
    }

    // Convert to array and filter out those with 0 discrepancies
    const sortedUsers = Object.values(userAgg).filter(u => u.discrepantLines > 0);

    // Sort based on selected sort condition
    sortedUsers.sort((a, b) => {
        let cmp = 0;
        if (sortVal === "stErrorRate") {
            const rateA = a.storesShared.size > 0 ? (a.storesDiscrepant.size / a.storesShared.size) : 0;
            const rateB = b.storesShared.size > 0 ? (b.storesDiscrepant.size / b.storesShared.size) : 0;
            cmp = rateB - rateA;
        } else if (sortVal === "qtyErrorRate") {
            const rateA = a.totalReqQty > 0 ? (a.totalDiffQty / a.totalReqQty) : 0;
            const rateB = b.totalReqQty > 0 ? (b.totalDiffQty / b.totalReqQty) : 0;
            cmp = rateB - rateA;
        } else if (sortVal === "totalDiffQty") {
            cmp = b.totalDiffQty - a.totalDiffQty;
        } else if (sortVal === "storesDiscrepant") {
            cmp = b.storesDiscrepant.size - a.storesDiscrepant.size;
        }
        const sizeA = a.storesDiscrepant.size;
        const sizeB = b.storesDiscrepant.size;
        return cmp || b.totalDiffQty - a.totalDiffQty || sizeB - sizeA || a.user.localeCompare(b.user, "vi");
    });

    // Slice to Top 10
    const top10 = sortedUsers.slice(0, 10);
    window.worstCTVNames = top10.map(item => item.user);

    if (top10.length === 0) {
        tbody.innerHTML = `<tr><td colspan="11" style="text-align: center; padding: 20px; color: var(--text-muted);">Không có CTV nào chia sai lệch</td></tr>`;
        return;
    }

    top10.forEach((item, index) => {
        const rank = index + 1;
        let rankBadge = rank;
        if (rank === 1) rankBadge = "🥇";
        else if (rank === 2) rankBadge = "🥈";
        else if (rank === 3) rankBadge = "🥉";

        const stErrorRate = item.storesShared.size > 0 ? ((item.storesDiscrepant.size / item.storesShared.size) * 100).toFixed(2) + "%" : "0.00%";
        const qtyErrorRate = item.totalReqQty > 0 ? ((item.totalDiffQty / item.totalReqQty) * 100).toFixed(2) + "%" : "0.00%";

        const tr = document.createElement("tr");
        let rowStyle = "";
        if (rank === 1) rowStyle = "background-color: rgba(253, 224, 71, 0.15); font-weight: 500;"; // soft gold
        else if (rank === 2) rowStyle = "background-color: rgba(226, 232, 240, 0.15);"; // soft silver
        else if (rank === 3) rowStyle = "background-color: rgba(217, 119, 6, 0.08);"; // soft bronze

        if (rowStyle) {
            tr.style = rowStyle;
        }

        tr.innerHTML = `
            <td style="text-align: center; font-size: 16px; font-weight: bold;">${rankBadge}</td>
            <td style="white-space: nowrap; font-size: 12px; color: var(--text-muted);">${formatActiveDates(item.dates)}</td>
            <td><strong>${item.user}</strong></td>
            <td style="text-align: right;">${formatNumber(item.storesShared.size)}</td>
            <td style="text-align: right; color: var(--color-danger); font-weight: bold;">${formatNumber(item.storesDiscrepant.size)}</td>
            <td style="text-align: right; font-weight: 500;">${stErrorRate}</td>
            <td style="text-align: right;">${formatNumber(item.totalSharedQty)}</td>
            <td style="text-align: right; color: var(--color-danger); font-weight: 500;">${formatNumber(item.totalDiffQty)}</td>
            <td style="text-align: right; font-weight: 500; color: var(--color-danger);">${qtyErrorRate}</td>
            <td style="text-align: right; font-weight: 500; color: var(--color-danger);">${formatNumber(item.diffQtyKg)}</td>
            <td style="text-align: right; font-weight: 500; color: var(--color-danger);">${formatNumber(item.diffQtyPack)}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Render summary of Top 10 CTVs with best performance (least discrepancies)
function renderTopCTVBestTable() {
    const tbody = document.getElementById("perfTopCTVBestBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    // Helper functions for dynamic prioritized sorting
    function getSortValueForCTV(userObj, prop) {
        switch (prop) {
            case "qtyErrorRate":
                return userObj.totalReqQty > 0 ? (userObj.totalDiffQty / userObj.totalReqQty) : 0;
            case "stErrorRate":
                return userObj.storesShared.size > 0 ? (userObj.storesDiscrepant.size / userObj.storesShared.size) : 0;
            case "totalSharedQty":
                return userObj.totalSharedQty;
            case "storesShared":
                return userObj.storesShared.size;
            case "totalDiffQty":
                return userObj.totalDiffQty;
            case "storesDiscrepant":
                return userObj.storesDiscrepant.size;
            default:
                return 0;
        }
    }

    function isAscendingSort(prop) {
        // Error rates and counts are sorted ascending (lowest is best)
        // Shared volume and store counts are sorted descending (highest is best)
        return prop === "qtyErrorRate" || prop === "stErrorRate" || prop === "totalDiffQty" || prop === "storesDiscrepant";
    }

    function compareCTVsByProp(a, b, prop) {
        const valA = getSortValueForCTV(a, prop);
        const valB = getSortValueForCTV(b, prop);
        if (valA === valB) return 0;
        
        const isAsc = isAscendingSort(prop);
        if (isAsc) {
            return valA - valB;
        } else {
            return valB - valA;
        }
    }

    // Extract performance active filter criteria
    const startDateQuery = document.getElementById("perfFilterStartDate") ? document.getElementById("perfFilterStartDate").value : "";
    const endDateQuery = document.getElementById("perfFilterEndDate") ? document.getElementById("perfFilterEndDate").value : "";
    const selectedUsers = Array.from(document.querySelectorAll("#perfFilterUserContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedToBranches = Array.from(document.querySelectorAll("#perfFilterToBranchContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedUnits = Array.from(document.querySelectorAll("#perfFilterUnitContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedGroups = Array.from(document.querySelectorAll("#perfFilterGroupContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const inputEl = document.getElementById("perfFilterItemCode");
    const textQuery = inputEl ? inputEl.value.toLowerCase().trim() : "";

    // Filter the shipping transfers (Tab 1 dataset) based on Tab 2 performance filters
    const activeTransfers = transfers.filter(t => {
        // Only evaluate main KHO RAU CỦ transfers for CTV performance reports
        if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") {
            return false;
        }
        // Keep only F1, F2, HUYHOANG, CTV, and exclude empty/unknown dividing staff
        if (!t.nguoiChia) {
            return false;
        }
        const name = t.nguoiChia.trim().toLowerCase();
        if (!(name.startsWith("f1") || name.startsWith("f2") || name.startsWith("huyhoang") || name.startsWith("ctv"))) {
            return false;
        }

        // Match staff group
        let matchGroup = true;
        if (selectedGroups.length > 0) {
            matchGroup = false;
            for (const g of selectedGroups) {
                if (name.startsWith(g.toLowerCase())) {
                    matchGroup = true;
                    break;
                }
            }
        }
        if (!matchGroup) return false;

        // Match items
        const matchItem = (selectedPerfItemCodes.length === 0 && textQuery === "") || 
            selectedPerfItemCodes.includes(t.itemCode) ||
            (textQuery !== "" && (t.itemCode.toLowerCase() === textQuery || t.itemName.toLowerCase() === textQuery));
        
        // Match user
        const matchUser = selectedUsers.length === 0 || selectedUsers.includes(t.nguoiChia);
        
        // Match to branch (Nơi nhận)
        const matchToBranch = selectedToBranches.length === 0 || selectedToBranches.includes(t.toBranch);
        
        // Match unit
        const matchUnit = selectedUnits.length === 0 || selectedUnits.includes(t.unit);
        
        // Match dates
        const matchStartDate = startDateQuery === "" || t.date >= startDateQuery;
        const matchEndDate = endDateQuery === "" || t.date <= endDateQuery;

        return matchItem && matchUser && matchToBranch && matchStartDate && matchEndDate && matchUnit;
    });

    // Aggregate discrepancy data by nguoiChia
    const userAgg = {};
    activeTransfers.forEach(t => {
        const user = t.nguoiChia || "Không rõ";
        if (!userAgg[user]) {
            userAgg[user] = {
                user: user,
                dates: new Set(),
                storesShared: new Set(),
                storesDiscrepant: new Set(),
                totalLines: 0,
                discrepantLines: 0,
                diffQtyKg: 0,
                diffQtyPack: 0,
                totalReqQty: 0,
                totalDiffQty: 0,
                totalSharedQty: 0
            };
        }
        if (t.date) {
            userAgg[user].dates.add(t.date);
        }

        const statusInfo = calculateStatus(t);
        
        // Skip in-transit rows from calculations
        if (statusInfo.statusText === "Đang chuyển") {
            return;
        }

        const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");

        if (t.toBranch) {
            const branchName = t.toBranch.trim();
            userAgg[user].storesShared.add(branchName);
            if (isDiscrepant) {
                userAgg[user].storesDiscrepant.add(branchName);
            }
        }

        userAgg[user].totalLines += 1;
        userAgg[user].totalReqQty += t.qtyShipped;
        userAgg[user].totalSharedQty += (t.qtyReceived + (t.matchedCorrectiveQty || 0));

        if (isDiscrepant) {
            userAgg[user].discrepantLines += 1;
            const absDiff = Math.abs(statusInfo.chenhLechConLai);
            userAgg[user].totalDiffQty += absDiff;
            
            const isKg = (t.unit && t.unit.toLowerCase() === "kg");
            if (isKg) {
                userAgg[user].diffQtyKg += absDiff;
            } else {
                userAgg[user].diffQtyPack += absDiff;
            }
        }
    });

    // Convert to array and exclude any users currently shown in the Top 10 wrong-divider table
    const worstCTVs = window.worstCTVNames || [];
    const allUsers = Object.values(userAgg).filter(u => !worstCTVs.includes(u.user));

    const sortSelect1 = document.getElementById("topCTVBestSort1");
    const sortSelect2 = document.getElementById("topCTVBestSort2");
    const sort1 = sortSelect1 ? sortSelect1.value : "qtyErrorRate";
    const sort2 = sortSelect2 ? sortSelect2.value : "totalSharedQty";

    // Sort based on selected priorities
    allUsers.sort((a, b) => {
        // Priority 1 Sort
        let cmp = compareCTVsByProp(a, b, sort1);
        if (cmp !== 0) return cmp;
        
        // Priority 2 Sort
        cmp = compareCTVsByProp(a, b, sort2);
        if (cmp !== 0) return cmp;
        
        // Fallbacks for stable sorting (volume desc, stores desc, name)
        cmp = compareCTVsByProp(a, b, "totalSharedQty");
        if (cmp !== 0) return cmp;
        
        cmp = compareCTVsByProp(a, b, "storesShared");
        if (cmp !== 0) return cmp;
        
        return a.user.localeCompare(b.user, "vi");
    });

    // Slice to Top 10
    const top10 = allUsers.slice(0, 10);

    if (top10.length === 0) {
        tbody.innerHTML = `<tr><td colspan="11" style="text-align: center; padding: 20px; color: var(--text-muted);">Không có dữ liệu CTV</td></tr>`;
        return;
    }

    top10.forEach((item, index) => {
        const rank = index + 1;
        let rankBadge = rank;
        if (rank === 1) rankBadge = "🥇";
        else if (rank === 2) rankBadge = "🥈";
        else if (rank === 3) rankBadge = "🥉";

        const stErrorRate = item.storesShared.size > 0 ? ((item.storesDiscrepant.size / item.storesShared.size) * 100).toFixed(2) + "%" : "0.00%";
        const qtyErrorRate = item.totalReqQty > 0 ? ((item.totalDiffQty / item.totalReqQty) * 100).toFixed(2) + "%" : "0.00%";

        const tr = document.createElement("tr");
        let rowStyle = "";
        if (rank === 1) rowStyle = "background-color: rgba(52, 211, 153, 0.15); font-weight: 500;"; // soft emerald/green
        else if (rank === 2) rowStyle = "background-color: rgba(226, 232, 240, 0.15);"; 
        else if (rank === 3) rowStyle = "background-color: rgba(217, 119, 6, 0.08);"; 

        if (rowStyle) {
            tr.style = rowStyle;
        }

        tr.innerHTML = `
            <td style="text-align: center; font-size: 16px; font-weight: bold;">${rankBadge}</td>
            <td style="white-space: nowrap; font-size: 12px; color: var(--text-muted);">${formatActiveDates(item.dates)}</td>
            <td><strong>${item.user}</strong></td>
            <td style="text-align: right;">${formatNumber(item.storesShared.size)}</td>
            <td style="text-align: right; color: var(--color-success); font-weight: bold;">${formatNumber(item.storesDiscrepant.size)}</td>
            <td style="text-align: right; font-weight: 500;">${stErrorRate}</td>
            <td style="text-align: right;">${formatNumber(item.totalSharedQty)}</td>
            <td style="text-align: right; color: var(--color-success); font-weight: 500;">${formatNumber(item.totalDiffQty)}</td>
            <td style="text-align: right; font-weight: 500; color: var(--color-success);">${qtyErrorRate}</td>
            <td style="text-align: right; font-weight: 500; color: var(--color-success);">${formatNumber(item.diffQtyKg)}</td>
            <td style="text-align: right; font-weight: 500; color: var(--color-success);">${formatNumber(item.diffQtyPack)}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Render summary of performance aggregated by CTV and Barcode/Item
function renderPerfSummaryTable() {
    const tbody = document.getElementById("perfSummaryBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    // Read summary inline filters
    const summaryFilterDate = document.getElementById("perfSummaryFilterDate") ? document.getElementById("perfSummaryFilterDate").value.toLowerCase().trim() : "";
    const summaryFilterUser = document.getElementById("perfSummaryFilterUser") ? document.getElementById("perfSummaryFilterUser").value.toLowerCase().trim() : "";
    const summaryFilterProduct = document.getElementById("perfSummaryFilterProduct") ? document.getElementById("perfSummaryFilterProduct").value.toLowerCase().trim() : "";
    const summaryFilterCategory = document.getElementById("perfSummaryFilterCategory") ? document.getElementById("perfSummaryFilterCategory").value.toLowerCase().trim() : "";
    const summaryFilterStatus = document.getElementById("perfSummaryFilterStatus") ? document.getElementById("perfSummaryFilterStatus").value : "";

    // Aggregate from the full performance dataset that matches top-level filters (both correct and discrepant)
    if (filteredPerfTransfers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 20px; color: var(--text-muted);">Không có dữ liệu tổng hợp phù hợp</td></tr>`;
        return;
    }

    // Build lookup for total shared quantity (unfiltered qtyShipped per date, user, barcode, unit)
    const totalSharedLookup = {};
    transfers.forEach(t => {
        if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") {
            return;
        }
        if (!t.nguoiChia) {
            return;
        }
        const user = t.nguoiChia.trim();
        const barcode = t.itemCode || "";
        const unit = t.unit || "";
        const date = t.date || "";
        const key = `${date}_${user}_${barcode}_${unit}`;
        
        if (!totalSharedLookup[key]) {
            totalSharedLookup[key] = 0;
        }
        totalSharedLookup[key] += t.qtyShipped;
    });

    // Group by key: date + '_' + nguoiChia + '_' + itemCode + '_' + unit
    const summaryAgg = {};
    filteredPerfTransfers.forEach(row => {
        const user = row.nguoiChia || "Không rõ";
        const barcode = row.itemCode || "";
        const unit = row.unit || "";
        const date = row.date || "";
        const key = `${date}_${user}_${barcode}_${unit}`;

        if (!summaryAgg[key]) {
            summaryAgg[key] = {
                date,
                user,
                barcode,
                itemName: row.itemName || "",
                unit,
                nganhHang: row.nganhHang || "",
                qtyReceived: 0,
                qtyShipped: 0,
                slBoSung: 0,
                chenhLechConLai: 0,
                absDiff: 0
            };
        }

        const statusInfo = calculateStatus(row);
        const receivedVal = row.qtyReceived === -1 ? 0 : row.qtyReceived;
        const slBoSung = row.matchedCorrectiveQty || 0;

        summaryAgg[key].qtyReceived += receivedVal;
        summaryAgg[key].qtyShipped += row.qtyShipped;
        summaryAgg[key].slBoSung += slBoSung;
        
        // Sum final discrepancies, ignoring normal "Hao hụt" (<15% KG) and "Đang chuyển"
        const statusText = statusInfo.statusText;
        const diff = (statusText === "Hao hụt" || statusText === "Đang chuyển") ? 0 : statusInfo.chenhLechConLai;
        summaryAgg[key].chenhLechConLai += diff;
        if (statusText === "Thiếu" || statusText === "Dư") {
            summaryAgg[key].absDiff += Math.abs(diff);
        }
    });

    let sortedSummary = Object.values(summaryAgg);

    // Apply inline summary table filters
    sortedSummary = sortedSummary.filter(item => {
        if (selectedSummaryProductCodes.length > 0 || summaryFilterProduct !== "") {
            const matchSelected = selectedSummaryProductCodes.length > 0 && selectedSummaryProductCodes.includes(item.barcode);
            
            let matchText = false;
            if (summaryFilterProduct !== "") {
                const barcodeClean = item.barcode.toLowerCase();
                const nameClean = removeVietnameseTones(item.itemName.toLowerCase());
                const queryClean = removeVietnameseTones(summaryFilterProduct);
                if (barcodeClean.includes(summaryFilterProduct) ||
                    item.itemName.toLowerCase().includes(summaryFilterProduct) ||
                    nameClean.includes(queryClean)) {
                    matchText = true;
                }
            }
            
            if (selectedSummaryProductCodes.length > 0) {
                if (!matchSelected && !matchText) return false;
            } else {
                if (!matchText) return false;
            }
        }
        
        // Apply summary inline filters (flexible date matching)
        if (summaryFilterDate !== "") {
            if (!matchDateQuery(item.date, summaryFilterDate)) return false;
        }

        if (summaryFilterUser !== "") {
            if (!item.user.toLowerCase().includes(summaryFilterUser)) return false;
        }

        if (summaryFilterProduct !== "") {
            const nameClean = removeVietnameseTones(item.itemName.toLowerCase());
            const queryClean = removeVietnameseTones(summaryFilterProduct);
            const barcodeClean = item.barcode.toLowerCase();
            if (!barcodeClean.includes(summaryFilterProduct) && 
                !item.itemName.toLowerCase().includes(summaryFilterProduct) && 
                !nameClean.includes(queryClean)) {
                return false;
            }
        }

        if (summaryFilterCategory !== "") {
            const catClean = removeVietnameseTones(item.nganhHang.toLowerCase());
            const queryClean = removeVietnameseTones(summaryFilterCategory);
            if (!item.nganhHang.toLowerCase().includes(summaryFilterCategory) && !catClean.includes(queryClean)) {
                return false;
            }
        }

        if (summaryFilterStatus !== "") {
            const diff = item.chenhLechConLai;
            if (summaryFilterStatus === "lệch" && diff === 0) return false;
            if (summaryFilterStatus === "thiếu" && diff >= 0) return false;
            if (summaryFilterStatus === "dư" && diff <= 0) return false;
            if (summaryFilterStatus === "đủ" && diff !== 0) return false;
        }

        return true;
    });

    if (sortedSummary.length === 0) {
        tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 20px; color: var(--text-muted);">Không có dữ liệu tổng hợp phù hợp</td></tr>`;
        return;
    }

    // Sort by date descending, then by user name, then by barcode
    sortedSummary.sort((a, b) => {
        const dateCmp = b.date.localeCompare(a.date);
        if (dateCmp !== 0) return dateCmp;
        const userCmp = a.user.localeCompare(b.user, "vi");
        if (userCmp !== 0) return userCmp;
        return a.barcode.localeCompare(b.barcode);
    });

    const displaySummary = sortedSummary.slice(0, 20);
    displaySummary.forEach((item, index) => {
        // Date formatting (timezone-independent)
        const formattedDate = formatDateToVN(item.date);

        const key = `${item.date}_${item.user}_${item.barcode}_${item.unit}`;
        const totalShared = totalSharedLookup[key] || 0;
        const diffStyle = item.chenhLechConLai < 0 
            ? 'color: var(--color-danger); font-weight: 500;' 
            : (item.chenhLechConLai > 0 ? 'color: var(--color-info); font-weight: 500;' : '');

        const pctLech = totalShared > 0 ? (item.chenhLechConLai / totalShared) * 100 : 0;
        let pctText = "0.00%";
        if (pctLech > 0) {
            pctText = `+${pctLech.toFixed(2)}%`;
        } else if (pctLech < 0) {
            pctText = `${pctLech.toFixed(2)}%`;
        }

        const pctStyle = item.chenhLechConLai < 0 
            ? 'color: var(--color-danger); font-weight: 500;' 
            : (item.chenhLechConLai > 0 ? 'color: var(--color-info); font-weight: 500;' : '');

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td style="text-align: center;">${index + 1}</td>
            <td>${formattedDate}</td>
            <td><strong>${item.user}</strong></td>
            <td><strong style="color: var(--color-primary);">${item.barcode}</strong></td>
            <td>${item.itemName}</td>
            <td>${item.unit}</td>
            <td>${item.nganhHang || "Khác"}</td>
            <td style="text-align: right; font-weight: 500;">${formatNumber(totalShared)}</td>
            <td style="text-align: right; ${diffStyle}">${formatDiffNumber(item.chenhLechConLai)}</td>
            <td style="text-align: right; ${pctStyle}">${pctText}</td>
        `;
        tbody.appendChild(tr);
    });
}


// Sorting logic for performance dataset
function sortFilteredPerfData() {
    filteredPerfTransfers.sort((a, b) => {
        let valA, valB;

        switch (currentPerfSortColumn) {
            case "ngayChuyen":
                valA = a.date || "";
                valB = b.date || "";
                break;
            case "maPhieu":
                valA = a.transferCode || "";
                valB = b.transferCode || "";
                break;
            case "noiNhan":
                valA = a.toBranch || "";
                valB = b.toBranch || "";
                break;
            case "barcode":
                valA = a.itemCode || "";
                valB = b.itemCode || "";
                break;
            case "tenSanPham":
                valA = a.itemName || "";
                valB = b.itemName || "";
                break;
            case "donVi":
                valA = a.unit || "";
                valB = b.unit || "";
                break;
            case "qtyShipped":
                valA = a.qtyShipped || 0;
                valB = b.qtyShipped || 0;
                break;
            case "qtyReceived":
                valA = a.qtyReceived || 0;
                valB = b.qtyReceived || 0;
                break;
            case "chenhLech":
                valA = a.qtyReceived - a.qtyShipped;
                valB = b.qtyReceived - b.qtyShipped;
                break;
            case "slBoSung":
                valA = a.matchedCorrectiveQty || 0;
                valB = b.matchedCorrectiveQty || 0;
                break;
            case "diff":
                valA = calculateStatus(a).chenhLechConLai;
                valB = calculateStatus(b).chenhLechConLai;
                break;
            case "nguoiChia":
                valA = a.nguoiChia || "";
                valB = b.nguoiChia || "";
                break;
            case "trangThai":
                valA = getPerfStatus(a);
                valB = getPerfStatus(b);
                break;
            default:
                valA = a[currentPerfSortColumn] || "";
                valB = b[currentPerfSortColumn] || "";
        }

        if (typeof valA === "string") {
            return currentPerfSortDirection === "asc" 
                ? valA.localeCompare(valB, "vi") 
                : valB.localeCompare(valA, "vi");
        } else {
            return currentPerfSortDirection === "asc" ? valA - valB : valB - valA;
        }
    });
}

// Get performance discrepant data after applying upper and inline filters
function getFilteredPerfDiscrepantData() {
    const dateFilterText = document.getElementById("perfTableFilterDate") ? document.getElementById("perfTableFilterDate").value.toLowerCase().trim() : "";
    const userFilterText = document.getElementById("perfTableFilterUser") ? document.getElementById("perfTableFilterUser").value.toLowerCase().trim() : "";
    const barcodeFilterText = document.getElementById("perfTableFilterBarcode") ? document.getElementById("perfTableFilterBarcode").value.toLowerCase().trim() : "";
    const nameFilterText = document.getElementById("perfTableFilterName") ? document.getElementById("perfTableFilterName").value.toLowerCase().trim() : "";
    const unitFilterText = document.getElementById("perfTableFilterUnit") ? document.getElementById("perfTableFilterUnit").value.toLowerCase().trim() : "";

    return filteredPerfTransfers.filter(row => {
        const statusInfo = calculateStatus(row);
        const diff = statusInfo.chenhLechConLai;
        if (diff === 0) return false;
        const status = statusInfo.statusText;
        if (status === "Hao hụt") return false;
        
        // Apply inline table filters
        if (dateFilterText !== "") {
            if (!matchDateQuery(row.date, dateFilterText)) return false;
        }
        if (userFilterText !== "") {
            const rowUser = (row.nguoiChia || "").toLowerCase();
            if (!rowUser.includes(userFilterText)) return false;
        }
        if (barcodeFilterText !== "") {
            const rowBarcode = (row.itemCode || "").toLowerCase();
            if (!rowBarcode.includes(barcodeFilterText)) return false;
        }
        if (nameFilterText !== "") {
            const rowName = (row.itemName || "").toLowerCase();
            const rowNameClean = removeVietnameseTones(rowName);
            const queryClean = removeVietnameseTones(nameFilterText);
            if (!rowName.includes(nameFilterText) && !rowNameClean.includes(queryClean)) return false;
        }
        if (unitFilterText !== "") {
            const rowUnit = (row.unit || "").toLowerCase();
            if (!rowUnit.includes(unitFilterText)) return false;
        }
        
        return true;
    });
}

// Render data table for Performance tab
function renderPerfTable() {
    const tbody = document.getElementById("perfTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    const discrepantData = getFilteredPerfDiscrepantData();

    if (discrepantData.length === 0) {
        tbody.innerHTML = `<tr><td colspan="14" style="text-align: center; padding: 40px; color: var(--text-muted);">Không có dòng lệch chia hàng phù hợp</td></tr>`;
        updatePerfPaginationUI(0);
        return;
    }

    const totalPages = Math.ceil(discrepantData.length / perfRowsPerPage);
    if (currentPerfPage > totalPages) currentPerfPage = totalPages;
    if (currentPerfPage < 1) currentPerfPage = 1;

    const startIndex = (currentPerfPage - 1) * perfRowsPerPage;
    const endIndex = Math.min(startIndex + perfRowsPerPage, discrepantData.length);
    const paginatedData = discrepantData.slice(startIndex, endIndex);

    paginatedData.forEach(row => {
        const statusInfo = calculateStatus(row);
        const diff = statusInfo.chenhLechConLai;
        const diffText = formatDiffNumber(diff);
        
        let diffStyle = '';
        if (diff < 0) {
            diffStyle = 'color: var(--color-danger); font-weight: 500;';
        } else if (diff > 0) {
            diffStyle = 'color: var(--color-info); font-weight: 500;';
        }

        // Date formatting (timezone-independent)
        const formattedDate = formatDateToVN(row.date);

        const status = getPerfStatus(row);
        let badgeClass = "badge-dang-chuyen";
        if (status === "Đã chia" || status === "Đủ") {
            badgeClass = "badge-du-ok";
        } else if (status === "Hao hụt") {
            badgeClass = "badge-haohut";
        } else if (status === "Thiếu") {
            badgeClass = "badge-thieu";
        } else if (status === "Dư") {
            badgeClass = "badge-du";
        }

        const rawDiff = row.qtyReceived - row.qtyShipped;
        const rawDiffText = formatDiffNumber(rawDiff);
        const slBoSung = row.matchedCorrectiveQty || 0;

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${formattedDate}</td>
            <td><strong>${row.transferCode}</strong></td>
            <td>${row.toBranch}</td>
            <td><strong style="color: var(--color-primary);">${row.itemCode}</strong></td>
            <td>${row.itemName}</td>
            <td>${row.unit}</td>
            <td>${row.nganhHang || "Khác"}</td>
            <td style="text-align: right; font-weight: 500;">${formatNumber(row.qtyShipped)}</td>
            <td style="text-align: right; font-weight: 500;">${formatNumber(row.qtyReceived)}</td>
            <td style="text-align: right; font-weight: 500;">${rawDiffText}</td>
            <td style="text-align: right; font-weight: 500; color: var(--color-primary);">${formatNumber(slBoSung)}</td>
            <td style="text-align: right; ${diffStyle}">${diffText}</td>
            <td><span style="font-weight:500;">${row.nguoiChia || "Không rõ"}</span></td>
            <td><span class="badge ${badgeClass}">${status}</span></td>
        `;
        tbody.appendChild(tr);
    });

    updatePerfPaginationUI(totalPages, startIndex + 1, endIndex, discrepantData.length);
}

function updatePerfPaginationUI(totalPages, fromIndex = 0, toIndex = 0, totalCount = 0) {
    const prevBtn = document.getElementById("perfPrevPageBtn");
    const nextBtn = document.getElementById("perfNextPageBtn");
    const infoText = document.getElementById("perfPaginationInfo");

    if (!prevBtn || !nextBtn || !infoText) return;

    if (totalCount === 0) {
        prevBtn.disabled = true;
        nextBtn.disabled = true;
        infoText.innerText = "Hiển thị 0 của 0 bản ghi";
        return;
    }

    prevBtn.disabled = currentPerfPage === 1;
    nextBtn.disabled = currentPerfPage === totalPages;
    infoText.innerText = `Hiển thị từ ${fromIndex} đến ${toIndex} của ${totalCount.toLocaleString()} bản ghi (Trang ${currentPerfPage}/${totalPages})`;
}

// Update stats count labels for Performance tab
function updatePerfSummary() {
    let totalReq = 0;
    let totalShared = 0;
    let totalDiff = 0;
    let totalDiffAbs = 0;

    const categories = ["2.VEGETABLES", "2.FRUITS", "2.BAKERY", "2.EGGS", "2.DELICA"];
    const categoryDiffs = {};
    categories.forEach(cat => {
        categoryDiffs[cat] = 0;
    });
    categoryDiffs["Khác"] = 0;

    filteredPerfTransfers.forEach(t => {
        totalReq += t.qtyShipped;
        totalShared += t.qtyReceived + (t.matchedCorrectiveQty || 0);
        
        const statusInfo = calculateStatus(t);
        const diff = statusInfo.chenhLechConLai;
        if (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư") {
            totalDiffAbs += Math.abs(diff);
        }
        if (diff < 0 && statusInfo.statusText !== "Hao hụt") {
            totalDiff += diff;
            const cat = t.nganhHang || "Khác";
            if (categories.includes(cat)) {
                categoryDiffs[cat] += diff;
            } else {
                categoryDiffs["Khác"] += diff;
            }
        }
    });

    const perfTotalReqEl = document.getElementById("perfTotalReq");
    const perfTotalSharedEl = document.getElementById("perfTotalShared");
    const perfTotalDiffEl = document.getElementById("perfTotalDiff");

    if (perfTotalReqEl) perfTotalReqEl.innerText = formatNumber(totalReq);
    if (perfTotalSharedEl) perfTotalSharedEl.innerText = formatNumber(totalShared);
    
    if (perfTotalDiffEl) {
        perfTotalDiffEl.innerText = formatDiffNumber(totalDiff);
        if (totalDiff < 0) {
            perfTotalDiffEl.style.color = "var(--color-danger)";
        } else if (totalDiff > 0) {
            perfTotalDiffEl.style.color = "var(--color-info)";
        } else {
            perfTotalDiffEl.style.color = "var(--text-primary)";
        }
    }
    
    // Calculate D-1 discrepancy rate
    const startEl = document.getElementById("perfFilterStartDate");
    const endEl = document.getElementById("perfFilterEndDate");
    const startVal = (startEl && startEl.value) ? startEl.value : earliestDate;
    const endVal = (endEl && endEl.value) ? endEl.value : latestDate;

    const prevStartDate = startVal ? getPrevDateStr(startVal) : "";
    const prevEndDate = endVal ? getPrevDateStr(endVal) : "";

    // Read selected filters for DOM-based D-1 filtering
    const selectedGroups = Array.from(document.querySelectorAll("#perfFilterGroupContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedUsers = Array.from(document.querySelectorAll("#perfFilterUserContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedStatuses = Array.from(document.querySelectorAll("#perfFilterStatusContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedToBranches = Array.from(document.querySelectorAll("#perfFilterToBranchContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedUnits = Array.from(document.querySelectorAll("#perfFilterUnitContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const selectedPerfCategories = Array.from(document.querySelectorAll("#perfFilterCategoryContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const inputEl = document.getElementById("perfFilterItemCode");
    const textQuery = inputEl ? inputEl.value.toLowerCase().trim() : "";

    function calculateErrorRateForRange(startDate, endDate) {
        let req = 0;
        let diffAbs = 0;
        
        const rangeTransfers = transfers.filter(t => {
            if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") {
                return false;
            }
            if (!t.nguoiChia) {
                return false;
            }
            const name = t.nguoiChia.trim().toLowerCase().normalize("NFC");
            const excluded = ["nhan quang hiếu", "nhân quang hiếu", "nhan quang hieu", "nhân quang hieu"];
            if (name === "" || excluded.includes(name)) {
                return false;
            }

            let matchGroup = true;
            if (selectedGroups.length > 0) {
                matchGroup = false;
                for (const g of selectedGroups) {
                    if (name.startsWith(g.toLowerCase())) {
                        matchGroup = true;
                        break;
                    }
                }
            }
            if (!matchGroup) return false;

            const statusInfo = calculateStatus(t);
            const status = statusInfo.statusText;

            const matchItem = (selectedPerfItemCodes.length === 0 && textQuery === "") || 
                selectedPerfItemCodes.includes(t.itemCode) ||
                (textQuery !== "" && (t.itemCode.toLowerCase() === textQuery || t.itemName.toLowerCase() === textQuery));
            
            const matchUser = selectedUsers.length === 0 || selectedUsers.includes(t.nguoiChia);
            const matchStatus = selectedStatuses.length === 0 || selectedStatuses.includes(status);
            const matchToBranch = selectedToBranches.length === 0 || selectedToBranches.includes(t.toBranch);
            const matchUnit = selectedUnits.length === 0 || selectedUnits.includes(t.unit);
            const matchCategory = selectedPerfCategories.length === 0 || selectedPerfCategories.includes(t.nganhHang);
            
            const matchStartDate = startDate === "" || t.date >= startDate;
            const matchEndDate = endDate === "" || t.date <= endDate;
            
            return matchItem && matchUser && matchStatus && matchToBranch && matchStartDate && matchEndDate && matchUnit && matchCategory;
        });
        
        rangeTransfers.forEach(t => {
            req += t.qtyShipped;
            const statusInfo = calculateStatus(t);
            const diff = statusInfo.chenhLechConLai;
            if (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư") {
                diffAbs += Math.abs(diff);
            }
        });
        
        return req > 0 ? (diffAbs / req) * 100 : 0;
    }

    const currentErrorRate = totalReq > 0 ? (totalDiffAbs / totalReq) * 100 : 0;
    const prevErrorRate = calculateErrorRateForRange(prevStartDate, prevEndDate);

    const perfTotalErrorRateEl = document.getElementById("perfTotalErrorRate");
    const perfTotalErrorRateD1El = document.getElementById("perfTotalErrorRateD1");

    if (perfTotalErrorRateEl) {
        perfTotalErrorRateEl.innerText = `${currentErrorRate.toFixed(2)}%`;
    }

    if (perfTotalErrorRateD1El) {
        if (prevStartDate && prevEndDate) {
            let hasD1Data = false;
            for (let i = 0; i < transfers.length; i++) {
                const t = transfers[i];
                if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() === "kho rau củ" && t.date >= prevStartDate && t.date <= prevEndDate) {
                    hasD1Data = true;
                    break;
                }
            }
            
            if (hasD1Data) {
                const diffRate = currentErrorRate - prevErrorRate;
                if (Math.abs(diffRate) < 0.005) {
                    perfTotalErrorRateD1El.innerHTML = `So với D-1: <span style="color: var(--text-muted); font-weight: 600;">—</span>`;
                } else if (diffRate > 0) {
                    perfTotalErrorRateD1El.innerHTML = `So với D-1: <span style="color: var(--color-danger); font-weight: 600;">▲ +${diffRate.toFixed(2)}%</span>`;
                } else {
                    perfTotalErrorRateD1El.innerHTML = `So với D-1: <span style="color: var(--color-success); font-weight: 600;">▼ ${diffRate.toFixed(2)}%</span>`;
                }
            } else {
                perfTotalErrorRateD1El.innerHTML = `So với D-1: <span style="color: var(--text-muted); font-weight: 600;">—</span>`;
            }
        } else {
            perfTotalErrorRateD1El.innerHTML = `So với D-1: <span style="color: var(--text-muted); font-weight: 600;">—</span>`;
        }
    }

    // Render category breakdown
    const breakdownEl = document.getElementById("perfCategoryDiffBreakdown");
    if (breakdownEl) {
        breakdownEl.innerHTML = "";
        
        const catOrder = ["2.VEGETABLES", "2.FRUITS", "2.BAKERY", "2.EGGS", "2.DELICA", "Khác"];
        
        catOrder.forEach(cat => {
            const val = categoryDiffs[cat] || 0;
            const catNameClean = cat.replace("2.", ""); // strip prefix for cleaner label
            
            const badge = document.createElement("div");
            badge.style.cssText = "display: flex; flex-direction: column; align-items: center; min-width: 100px; padding: 8px 12px; border-radius: var(--radius-md); background-color: var(--bg-primary); border: 1px solid var(--border-color); flex: 1; min-width: 120px; box-shadow: var(--shadow-sm);";
            
            const labelEl = document.createElement("span");
            labelEl.style.cssText = "font-size: 10px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;";
            labelEl.innerText = catNameClean;
            
            const valEl = document.createElement("span");
            valEl.style.cssText = `font-size: 15px; font-weight: 700; margin-top: 4px;`;
            if (val < 0) {
                valEl.style.color = "var(--color-danger)";
                valEl.innerText = formatDiffNumber(val);
            } else {
                valEl.style.color = "var(--text-muted)";
                valEl.innerText = "0";
            }
            
            badge.appendChild(labelEl);
            badge.appendChild(valEl);
            breakdownEl.appendChild(badge);
        });
    }
}

// Export performance report to CSV
function exportPerfToCSV() {
    const discrepantData = getFilteredPerfDiscrepantData();

    if (discrepantData.length === 0) {
        alert("Không có dữ liệu lệch để xuất!");
        return;
    }

    let csvContent = "\uFEFF"; // UTF-8 BOM representation
    csvContent += "Ngày chuyển,Mã Phiếu,Nơi nhận,Barcode,Tên sản phẩm,Đơn vị,Ngành hàng,SL chuyển,SL nhận,Chênh lệch,Bổ sung,CL còn lại,Người chia hàng,Trạng thái\n";

    discrepantData.forEach(t => {
        const statusInfo = calculateStatus(t);
        const diff = statusInfo.chenhLechConLai;
        const rawDiff = t.qtyReceived - t.qtyShipped;
        const slBoSung = t.matchedCorrectiveQty || 0;

        const row = [
            t.date,
            `"${t.transferCode.replace(/"/g, '""')}"`,
            `"${t.toBranch.replace(/"/g, '""')}"`,
            `"${t.itemCode.replace(/"/g, '""')}"`,
            `"${t.itemName.replace(/"/g, '""')}"`,
            `"${t.unit.replace(/"/g, '""')}"`,
            `"${(t.nganhHang || "Khác").replace(/"/g, '""')}"`,
            t.qtyShipped,
            t.qtyReceived,
            rawDiff,
            slBoSung,
            diff,
            `"${(t.nguoiChia || "").replace(/"/g, '""')}"`,
            `"${getPerfStatus(t)}"`
        ];
        csvContent += row.join(",") + "\n";
    });

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    
    const todayStr = new Date().toISOString().split("T")[0];
    link.setAttribute("download", `BaoCao_HieuSuatChiaHang_${todayStr}.csv`);
    link.style.visibility = "hidden";
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Bảng theo dõi hiệu suất phân loại theo Ngành Hàng (Nhóm F1)
function renderF1CategoryTable() {
    const tbody = document.getElementById("perfF1CategoryBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    const contentCategoryPerformance = document.getElementById("contentCategoryPerformance");
    const isCategoryTabActive = contentCategoryPerformance && contentCategoryPerformance.classList.contains("active");

    const groupSelector = isCategoryTabActive ? "#catFilterGroupContainer input[type='checkbox']:checked" : "#perfFilterGroupContainer input[type='checkbox']:checked";
    const selectedGroups = Array.from(document.querySelectorAll(groupSelector)).map(cb => cb.value);
    
    let activeGroups = [];
    const groupFilterEl = document.getElementById("perfF1GroupFilter");
    const groupFilterVal = groupFilterEl ? groupFilterEl.value : "All";

    if (selectedGroups.length > 0) {
        activeGroups = selectedGroups;
        if (groupFilterEl) {
            if (selectedGroups.length === 1) {
                groupFilterEl.value = selectedGroups[0];
            } else {
                groupFilterEl.value = "All";
            }
        }
    } else {
        if (groupFilterVal === "All") {
            activeGroups = ["F1", "F2", "HUYHOANG", "CTV"];
        } else {
            activeGroups = [groupFilterVal];
        }
    }

    const titleGroupText = activeGroups.join(" + ");
    const headerGroupText = activeGroups.join("/");

    const titleEl = document.getElementById("perfF1TableTitle");
    if (titleEl) {
        const isAllGroups = activeGroups.length === 4 && 
                            activeGroups.includes("F1") && 
                            activeGroups.includes("F2") && 
                            activeGroups.includes("HUYHOANG") && 
                            activeGroups.includes("CTV");
        if (isAllGroups) {
            titleEl.innerHTML = "📊 Theo dõi hiệu suất phân loại theo Ngành Hàng (Toàn bộ nhân sự)";
        } else {
            titleEl.innerHTML = `📊 Theo dõi hiệu suất phân loại theo Ngành Hàng (Nhóm ${titleGroupText})`;
        }
    }

    const tableStartEl = document.getElementById("perfF1CategoryStartDate");
    const tableEndEl = document.getElementById("perfF1CategoryEndDate");
    const globalStartEl = document.getElementById(isCategoryTabActive ? "catFilterStartDate" : "perfFilterStartDate");
    const globalEndEl = document.getElementById(isCategoryTabActive ? "catFilterEndDate" : "perfFilterEndDate");

    const startDateQuery = (tableStartEl && tableStartEl.value) ? tableStartEl.value : (globalStartEl ? globalStartEl.value : "");
    const endDateQuery = (tableEndEl && tableEndEl.value) ? tableEndEl.value : (globalEndEl ? globalEndEl.value : "");
    
    const perfF1CategoryFilterDate = document.getElementById("perfF1CategoryFilterDate") ? document.getElementById("perfF1CategoryFilterDate").value.toLowerCase().trim() : "";
    
    const selectedUsers = isCategoryTabActive ? [] : Array.from(document.querySelectorAll("#perfFilterUserContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const localUserSearch = document.getElementById("perfF1UserSearch") ? document.getElementById("perfF1UserSearch").value.toLowerCase().trim() : "";

    const activeTransfers = transfers.filter(t => {
        if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") {
            return false;
        }
        if (!t.nguoiChia) {
            return false;
        }
        const name = t.nguoiChia.trim().toLowerCase();
        
        let matchGroupPrefix = false;
        for (const g of activeGroups) {
            if (name.startsWith(g.toLowerCase())) {
                matchGroupPrefix = true;
                break;
            }
        }
        if (!matchGroupPrefix) return false;

        // Match global user selection (only if not on the dedicated Category tab)
        const matchUser = selectedUsers.length === 0 || selectedUsers.includes(t.nguoiChia);
        if (!matchUser) return false;

        // Match local user search box
        if (localUserSearch !== "") {
            if (!name.includes(localUserSearch)) {
                return false;
            }
        }

        // Match dates
        const matchStartDate = startDateQuery === "" || t.date >= startDateQuery;
        const matchEndDate = endDateQuery === "" || t.date <= endDateQuery;
        const matchFilterDate = perfF1CategoryFilterDate === "" || matchDateQuery(t.date, perfF1CategoryFilterDate);

        return matchStartDate && matchEndDate && matchFilterDate;
    });
    lastActiveTransfers = activeTransfers;

    if (activeTransfers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="12" style="text-align: center; padding: 20px; color: var(--text-muted);">Không có dữ liệu cho nhân sự ${headerGroupText}</td></tr>`;
        return;
    }

    const categories = ["2.VEGETABLES", "2.FRUITS", "2.BAKERY", "2.EGGS", "2.DELICA"];

    const userAgg = {};
    activeTransfers.forEach(t => {
        const user = t.nguoiChia.trim();
        const cat = t.nganhHang || "Khác";
        
        if (!userAgg[user]) {
            userAgg[user] = {
                user: user,
                categories: {}
            };
            categories.forEach(c => {
                userAgg[user].categories[c] = {
                    shipped: 0,
                    received: 0,
                    diff: 0
                };
            });
        }

        const statusInfo = calculateStatus(t);
        if (statusInfo.statusText === "Đang chuyển") {
            return;
        }

        if (categories.includes(cat)) {
            const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");
            userAgg[user].categories[cat].shipped += t.qtyShipped;
            userAgg[user].categories[cat].received += t.qtyReceived + (t.matchedCorrectiveQty || 0);
            if (isDiscrepant) {
                userAgg[user].categories[cat].diff += Math.abs(statusInfo.chenhLechConLai);
            }
        }
    });

    const sortedUsers = Object.keys(userAgg).sort((a, b) => a.localeCompare(b, "vi"));
    const displayUsers = sortedUsers.slice(0, 20);

    displayUsers.forEach((user, index) => {
        const uData = userAgg[user];
        
        const catRates = categories.map(cat => {
            const shipped = uData.categories[cat].shipped;
            const diff = uData.categories[cat].diff;
            const errorRate = shipped > 0 ? (diff / shipped) * 100 : 0;
            return {
                category: cat,
                errorRate: errorRate,
                shipped: shipped
            };
        });

        // Calculate aggregate totals for the 5 target categories
        let totalShipped = 0;
        let totalReceived = 0;
        let totalDiff = 0;
        categories.forEach(cat => {
            totalShipped += uData.categories[cat].shipped;
            totalReceived += uData.categories[cat].received;
            totalDiff += uData.categories[cat].diff;
        });
        const totalErrorRate = totalShipped > 0 ? (totalDiff / totalShipped) * 100 : 0;

        const getStyleForCat = (rateVal, qtyVal, isTotal = false) => {
            if (qtyVal === 0) {
                return "text-align: right;";
            }
            if (isTotal) {
                // Total column threshold: > 2000 -> 0.5% tolerance, <= 2000 -> 0.2% tolerance
                // (low error < tolerance is green, high error >= tolerance is red)
                const limit = qtyVal > 2000 ? 0.5 : 0.2;
                if (rateVal < limit) {
                    return "background-color: rgba(16, 185, 129, 0.15); color: var(--color-success); font-weight: bold; text-align: right;";
                } else {
                    return "background-color: rgba(239, 68, 68, 0.15); color: var(--color-danger); font-weight: bold; text-align: right;";
                }
            } else {
                // Category-wise threshold: > 500 -> 0.2%/0.5% thresholds, <= 500 -> 0.1% threshold
                if (qtyVal > 500) {
                    if (rateVal < 0.2) {
                        return "background-color: rgba(16, 185, 129, 0.15); color: var(--color-success); font-weight: bold; text-align: right;";
                    } else if (rateVal <= 0.5) {
                        return "background-color: rgba(245, 158, 11, 0.15); color: var(--color-warning); font-weight: bold; text-align: right;";
                    } else {
                        return "background-color: rgba(239, 68, 68, 0.15); color: var(--color-danger); font-weight: bold; text-align: right;";
                    }
                } else {
                    if (rateVal < 0.1) {
                        return "background-color: rgba(16, 185, 129, 0.15); color: var(--color-success); font-weight: bold; text-align: right;";
                    } else {
                        return "background-color: rgba(239, 68, 68, 0.15); color: var(--color-danger); font-weight: bold; text-align: right;";
                    }
                }
            }
        };

        const tr = document.createElement("tr");
        let htmlContent = `
            <td style="text-align: center;">${index + 1}</td>
            <td><strong>${user}</strong></td>
        `;

        categories.forEach(cat => {
            const qtyVal = uData.categories[cat].shipped;
            htmlContent += `<td style="text-align: right;">${formatNumber(qtyVal)}</td>`;
        });
        // Add total quantity column cell (with a left border)
        htmlContent += `<td style="text-align: right; font-weight: bold; border-left: 1px solid var(--border-color); color: var(--color-primary);">${formatNumber(totalShipped)}</td>`;

        categories.forEach(cat => {
            const catRateObj = catRates.find(item => item.category === cat);
            const rateVal = catRateObj.errorRate;
            const qtyVal = catRateObj.shipped;
            const style = getStyleForCat(rateVal, qtyVal);
            const displayText = qtyVal === 0 ? "" : `${rateVal.toFixed(2)}%`;
            htmlContent += `<td style="${style}">${displayText}</td>`;
        });
        // Add total error rate column cell (with a left border and coloring based on thresholds)
        const totalStyle = getStyleForCat(totalErrorRate, totalShipped, true) + " font-weight: bold; border-left: 1px solid var(--border-color);";
        const totalDisplayText = totalShipped === 0 ? "" : `${totalErrorRate.toFixed(2)}%`;
        htmlContent += `<td style="${totalStyle}">${totalDisplayText}</td>`;

        tr.innerHTML = htmlContent;
        tbody.appendChild(tr);
    });
    renderF1CategoryDateTable();
    renderVegetablesLevel3DateTable();
    renderVegetablesLevel3Table();
    renderTopSkuDiscrepancyTable();
}

// ============================================================
// Bảng chi tiết hiệu suất nhóm hàng Rau Củ (Level 3 - 2.VEGETABLES)
// ============================================================
function renderVegetablesLevel3Table() {
    const tbody = document.getElementById("vegLevel3Body");
    if (!tbody) return;
    tbody.innerHTML = "";

    const contentCategoryPerformance = document.getElementById("contentCategoryPerformance");
    const isCategoryTabActive = contentCategoryPerformance && contentCategoryPerformance.classList.contains("active");

    const groupSelector = isCategoryTabActive ? "#catFilterGroupContainer input[type='checkbox']:checked" : "#perfFilterGroupContainer input[type='checkbox']:checked";
    const selectedGroups = Array.from(document.querySelectorAll(groupSelector)).map(cb => cb.value);
    
    let activeGroups = [];
    const groupFilterEl = document.getElementById("perfF1GroupFilter");
    const groupFilterVal = groupFilterEl ? groupFilterEl.value : "All";

    if (selectedGroups.length > 0) {
        activeGroups = selectedGroups;
    } else {
        if (groupFilterVal === "All") {
            activeGroups = ["F1", "F2", "HUYHOANG", "CTV"];
        } else {
            activeGroups = [groupFilterVal];
        }
    }

    const tableStartEl = document.getElementById("vegLevel3StartDate");
    const tableEndEl = document.getElementById("vegLevel3EndDate");

    const specificStart = tableStartEl ? tableStartEl.value : "";
    const specificEnd = tableEndEl ? tableEndEl.value : "";
    
    let startDateQuery = "";
    let endDateQuery = "";
    
    if (specificStart === "" && specificEnd === "") {
        startDateQuery = latestDate;
        endDateQuery = latestDate;
    } else {
        startDateQuery = specificStart;
        endDateQuery = specificEnd;
    }

    const selectedUsers = isCategoryTabActive ? [] : Array.from(document.querySelectorAll("#perfFilterUserContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const localUserSearch = document.getElementById("perfF1UserSearch") ? document.getElementById("perfF1UserSearch").value.toLowerCase().trim() : "";

    const filteredTransfers = transfers.filter(t => {
        if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") {
            return false;
        }
        if (!t.nguoiChia) {
            return false;
        }
        const name = t.nguoiChia.trim().toLowerCase();
        
        let matchGroupPrefix = false;
        for (const g of activeGroups) {
            if (name.startsWith(g.toLowerCase())) {
                matchGroupPrefix = true;
                break;
            }
        }
        if (!matchGroupPrefix) return false;

        const matchUser = selectedUsers.length === 0 || selectedUsers.includes(t.nguoiChia);
        if (!matchUser) return false;

        if (localUserSearch !== "") {
            if (!name.includes(localUserSearch)) {
                return false;
            }
        }

        return true;
    });

    const vegLevel3FilterDate = document.getElementById("vegLevel3FilterDate") ? document.getElementById("vegLevel3FilterDate").value.toLowerCase().trim() : "";

    const level3Cats = [
        "3.ROOT VEGGIES",
        "3.FRUIT VEGGIES",
        "3.LEAFY VEGGIES",
        "3.PROCESSED VEGGIES",
        "3.HERBS",
        "3.LETTUCE, SNACKABLES",
        "3.MUSHROOM"
    ];

    // Group by Date + Level 3 category for ALL dates
    const allGroupAgg = {};
    filteredTransfers.forEach(t => {
        if (t.nganhHang !== "2.VEGETABLES") {
            return;
        }
        const level3 = t.subCategoryLevel3 || "";
        if (!level3 || !level3Cats.includes(level3)) {
            return;
        }

        const statusInfo = calculateStatus(t);
        if (statusInfo.statusText === "Đang chuyển") {
            return;
        }

        const date = t.date || "";
        const key = `${date}_${level3}`;

        if (!allGroupAgg[key]) {
            allGroupAgg[key] = {
                shipped: 0,
                diff: 0
            };
        }

        allGroupAgg[key].shipped += t.qtyShipped;
        const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");
        if (isDiscrepant) {
            allGroupAgg[key].diff += Math.abs(statusInfo.chenhLechConLai);
        }
    });

    // Extract selected period subset
    const groupAgg = {};
    for (const key in allGroupAgg) {
        const parts = key.split("_");
        const date = parts[0];
        const level3 = parts[1];

        const matchStartDate = startDateQuery === "" || date >= startDateQuery;
        const matchEndDate = endDateQuery === "" || date <= endDateQuery;

        if (matchStartDate && matchEndDate) {
            groupAgg[key] = {
                date,
                level3,
                shipped: allGroupAgg[key].shipped,
                diff: allGroupAgg[key].diff
            };
        }
    }

    let sortedSummary = Object.values(groupAgg);

    // Apply quick inline date filter
    if (vegLevel3FilterDate !== "") {
        sortedSummary = sortedSummary.filter(item => {
            return matchDateQuery(item.date, vegLevel3FilterDate);
        });
    }

    // Sort by Date descending, then by Level 3 category name
    sortedSummary.sort((a, b) => {
        const dateCmp = b.date.localeCompare(a.date);
        if (dateCmp !== 0) return dateCmp;
        return a.level3.localeCompare(b.level3);
    });

    if (sortedSummary.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 20px; color: var(--text-muted);">Không có dữ liệu phù hợp</td></tr>`;
        return;
    }

    const getRateStyle = (rateVal, qtyVal) => {
        if (qtyVal === 0) return "text-align: right;";
        if (rateVal > 0.5) {
            return "background-color: rgba(239, 68, 68, 0.15); color: var(--color-danger); font-weight: bold; text-align: right;";
        } else if (rateVal < 0.2) {
            return "background-color: rgba(16, 185, 129, 0.15); color: var(--color-success); font-weight: bold; text-align: right;";
        } else {
            return "background-color: rgba(245, 158, 11, 0.15); color: var(--color-warning); font-weight: bold; text-align: right;";
        }
    };

    sortedSummary.forEach((item, index) => {
        const formattedDate = formatDateToVN(item.date);
        const shipped = item.shipped;
        const diff = item.diff;
        const errorRate = shipped > 0 ? (diff / shipped) * 100 : 0;
        const rateStyle = getRateStyle(errorRate, shipped);

        // D-1 comparison calculations
        let prevRateText = "—";
        let prevRateStyle = "text-align: right; color: var(--text-muted);";
        let statusHtml = `<span style="color: var(--text-muted);">—</span>`;

        const prevDate = getPrevDateStr(item.date);
        const d1Key = `${prevDate}_${item.level3}`;
        const prevItem = allGroupAgg[d1Key];

        if (prevItem && prevItem.shipped > 0) {
            const prevShipped = prevItem.shipped;
            const prevDiff = prevItem.diff;
            const prevRateVal = (prevDiff / prevShipped) * 100;
            prevRateText = prevRateVal.toFixed(2) + "%";
            prevRateStyle = getRateStyle(prevRateVal, prevShipped);

            const diffRate = errorRate - prevRateVal;
            if (Math.abs(diffRate) < 0.005) {
                statusHtml = `<span style="color: var(--text-muted);">—</span>`;
            } else if (diffRate > 0) {
                statusHtml = `<span style="color: var(--color-danger); font-weight: 600;">▲ +${diffRate.toFixed(2)}%</span>`;
            } else {
                statusHtml = `<span style="color: var(--color-success); font-weight: 600;">▼ ${diffRate.toFixed(2)}%</span>`;
            }
        }

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td style="text-align: center;">${index + 1}</td>
            <td>${formattedDate}</td>
            <td style="font-weight: 600; color: var(--text-primary);">${item.level3}</td>
            <td style="text-align: right; font-weight: 500;">${formatNumber(shipped)}</td>
            <td style="text-align: right; color: ${diff > 0 ? 'var(--color-danger)' : 'var(--text-muted)'}; font-weight: 500;">${formatDiffNumber(diff)}</td>
            <td style="${rateStyle}">${shipped > 0 ? errorRate.toFixed(2) + "%" : "0.00%"}</td>
            <td style="${prevRateStyle}">${prevRateText}</td>
            <td style="text-align: center; font-size: 13px;">${statusHtml}</td>
        `;
        tbody.appendChild(tr);
    });

    // Bind export button click listener
    const perfVegLevel3BtnExport = document.getElementById("perfVegLevel3BtnExport");
    if (perfVegLevel3BtnExport) {
        const newBtn = perfVegLevel3BtnExport.cloneNode(true);
        perfVegLevel3BtnExport.parentNode.replaceChild(newBtn, perfVegLevel3BtnExport);
        newBtn.addEventListener("click", () => {
            const todayStr = new Date().toISOString().split("T")[0];
            downloadTableToExcel("vegLevel3Table", `BaoCao_HieuSuatRauCu_Level3_${todayStr}.csv`);
        });
    }
}

// ============================================================
// Bảng theo dõi hiệu suất phân loại theo Ngày & Ngành Hàng
// ============================================================
function renderF1CategoryDateTable() {
    const tbody = document.getElementById("perfF1CategoryDateBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    const contentCategoryPerformance = document.getElementById("contentCategoryPerformance");
    const isCategoryTabActive = contentCategoryPerformance && contentCategoryPerformance.classList.contains("active");

    const groupSelector = isCategoryTabActive ? "#catFilterGroupContainer input[type='checkbox']:checked" : "#perfFilterGroupContainer input[type='checkbox']:checked";
    const selectedGroups = Array.from(document.querySelectorAll(groupSelector)).map(cb => cb.value);
    
    let activeGroups = [];
    const groupFilterEl = document.getElementById("perfF1GroupFilter");
    const groupFilterVal = groupFilterEl ? groupFilterEl.value : "All";

    if (selectedGroups.length > 0) {
        activeGroups = selectedGroups;
    } else {
        if (groupFilterVal === "All") {
            activeGroups = ["F1", "F2", "HUYHOANG", "CTV"];
        } else {
            activeGroups = [groupFilterVal];
        }
    }

    const tableStartEl = document.getElementById("catDateTableStartDate");
    const tableEndEl = document.getElementById("catDateTableEndDate");
    const globalStartEl = document.getElementById(isCategoryTabActive ? "catFilterStartDate" : "perfFilterStartDate");
    const globalEndEl = document.getElementById(isCategoryTabActive ? "catFilterEndDate" : "perfFilterEndDate");

    const startDateQuery = (tableStartEl && tableStartEl.value) ? tableStartEl.value : (globalStartEl ? globalStartEl.value : "");
    const endDateQuery = (tableEndEl && tableEndEl.value) ? tableEndEl.value : (globalEndEl ? globalEndEl.value : "");
    
    const selectedUsers = isCategoryTabActive ? [] : Array.from(document.querySelectorAll("#perfFilterUserContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const localUserSearch = document.getElementById("perfF1UserSearch") ? document.getElementById("perfF1UserSearch").value.toLowerCase().trim() : "";

    const activeTransfers = transfers.filter(t => {
        if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") {
            return false;
        }
        if (!t.nguoiChia) {
            return false;
        }
        const name = t.nguoiChia.trim().toLowerCase();
        
        let matchGroupPrefix = false;
        for (const g of activeGroups) {
            if (name.startsWith(g.toLowerCase())) {
                matchGroupPrefix = true;
                break;
            }
        }
        if (!matchGroupPrefix) return false;

        const matchUser = selectedUsers.length === 0 || selectedUsers.includes(t.nguoiChia);
        if (!matchUser) return false;

        if (localUserSearch !== "") {
            if (!name.includes(localUserSearch)) {
                return false;
            }
        }

        const matchStartDate = startDateQuery === "" || t.date >= startDateQuery;
        const matchEndDate = endDateQuery === "" || t.date <= endDateQuery;

        return matchStartDate && matchEndDate;
    });

    if (activeTransfers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 20px; color: var(--text-muted);">Không có dữ liệu phù hợp</td></tr>`;
        return;
    }

    const categories = ["2.VEGETABLES", "2.FRUITS", "2.BAKERY", "2.EGGS", "2.DELICA"];
    const dateAgg = {};

    activeTransfers.forEach(t => {
        const date = t.date;
        const cat = t.nganhHang || "Khác";

        if (!dateAgg[date]) {
            dateAgg[date] = {
                date: date,
                categories: {}
            };
            categories.forEach(c => {
                dateAgg[date].categories[c] = { shipped: 0, received: 0, diff: 0 };
            });
        }

        const statusInfo = calculateStatus(t);
        if (statusInfo.statusText === "Đang chuyển") {
            return;
        }

        if (categories.includes(cat)) {
            const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");
            dateAgg[date].categories[cat].shipped += t.qtyShipped;
            dateAgg[date].categories[cat].received += t.qtyReceived + (t.matchedCorrectiveQty || 0);
            if (isDiscrepant) {
                dateAgg[date].categories[cat].diff += Math.abs(statusInfo.chenhLechConLai);
            }
        }
    });

    const sortedDates = Object.keys(dateAgg).sort();

    const getStyleForDailyCat = (rateVal, qtyVal) => {
        if (qtyVal === 0) return "text-align: right;";
        if (rateVal < 0.2) {
            return "background-color: rgba(16, 185, 129, 0.15); color: var(--color-success); font-weight: bold; text-align: right;";
        } else if (rateVal <= 0.5) {
            return "background-color: rgba(245, 158, 11, 0.15); color: var(--color-warning); font-weight: bold; text-align: right;";
        } else {
            return "background-color: rgba(239, 68, 68, 0.15); color: var(--color-danger); font-weight: bold; text-align: right;";
        }
    };

    const localDateSearch = document.getElementById("catDateTableFilterDate") ? document.getElementById("catDateTableFilterDate").value.trim() : "";
    let displayIndex = 1;

    sortedDates.forEach((date) => {
        const formattedDate = formatDateToVN(date);
        if (localDateSearch !== "") {
            if (!formattedDate.includes(localDateSearch)) {
                return;
            }
        }

        const dData = dateAgg[date];
        const tr = document.createElement("tr");

        let htmlContent = `
            <td style="text-align: center;">${displayIndex++}</td>
            <td><strong>${formattedDate}</strong></td>
        `;

        let totalShipped = 0;
        let totalReceived = 0;
        let totalDiff = 0;

        categories.forEach(cat => {
            totalShipped += dData.categories[cat].shipped;
            totalReceived += dData.categories[cat].received;
            totalDiff += dData.categories[cat].diff;
        });

        categories.forEach(cat => {
            const shipped = dData.categories[cat].shipped;
            const diff = dData.categories[cat].diff;
            const rateVal = shipped > 0 ? (diff / shipped) * 100 : 0;
            const style = getStyleForDailyCat(rateVal, shipped);
            const displayText = shipped === 0 ? "0.00%" : `${rateVal.toFixed(2)}%`;
            htmlContent += `<td style="${style}">${displayText}</td>`;
        });

        const totalErrorRate = totalShipped > 0 ? (totalDiff / totalShipped) * 100 : 0;
        const totalStyle = getStyleForDailyCat(totalErrorRate, totalShipped) + " font-weight: bold; border-left: 1px solid var(--border-color);";
        const totalDisplayText = totalShipped === 0 ? "0.00%" : `${totalErrorRate.toFixed(2)}%`;
        htmlContent += `<td style="${totalStyle}">${totalDisplayText}</td>`;

        tr.innerHTML = htmlContent;
        tbody.appendChild(tr);
    });
}

// ============================================================
// Bảng theo dõi hiệu suất phân loại theo Ngày & Ngành Hàng Rau Củ (Level 3)
// ============================================================
function renderVegetablesLevel3DateTable() {
    const tbody = document.getElementById("perfVegLevel3DateBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    const contentCategoryPerformance = document.getElementById("contentCategoryPerformance");
    const isCategoryTabActive = contentCategoryPerformance && contentCategoryPerformance.classList.contains("active");

    const groupSelector = isCategoryTabActive ? "#catFilterGroupContainer input[type='checkbox']:checked" : "#perfFilterGroupContainer input[type='checkbox']:checked";
    const selectedGroups = Array.from(document.querySelectorAll(groupSelector)).map(cb => cb.value);
    
    let activeGroups = [];
    const groupFilterEl = document.getElementById("perfF1GroupFilter");
    const groupFilterVal = groupFilterEl ? groupFilterEl.value : "All";

    if (selectedGroups.length > 0) {
        activeGroups = selectedGroups;
    } else {
        if (groupFilterVal === "All") {
            activeGroups = ["F1", "F2", "HUYHOANG", "CTV"];
        } else {
            activeGroups = [groupFilterVal];
        }
    }

    const tableStartEl = document.getElementById("vegLevel3DateStartDate");
    const tableEndEl = document.getElementById("vegLevel3DateEndDate");
    const globalStartEl = document.getElementById(isCategoryTabActive ? "catFilterStartDate" : "perfFilterStartDate");
    const globalEndEl = document.getElementById(isCategoryTabActive ? "catFilterEndDate" : "perfFilterEndDate");

    const startDateQuery = (tableStartEl && tableStartEl.value) ? tableStartEl.value : (globalStartEl ? globalStartEl.value : "");
    const endDateQuery = (tableEndEl && tableEndEl.value) ? tableEndEl.value : (globalEndEl ? globalEndEl.value : "");
    
    const selectedUsers = isCategoryTabActive ? [] : Array.from(document.querySelectorAll("#perfFilterUserContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const localUserSearch = document.getElementById("perfF1UserSearch") ? document.getElementById("perfF1UserSearch").value.toLowerCase().trim() : "";

    const activeTransfers = transfers.filter(t => {
        if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") {
            return false;
        }
        if (!t.nguoiChia) {
            return false;
        }
        const name = t.nguoiChia.trim().toLowerCase();
        
        let matchGroupPrefix = false;
        for (const g of activeGroups) {
            if (name.startsWith(g.toLowerCase())) {
                matchGroupPrefix = true;
                break;
            }
        }
        if (!matchGroupPrefix) return false;

        const matchUser = selectedUsers.length === 0 || selectedUsers.includes(t.nguoiChia);
        if (!matchUser) return false;

        if (localUserSearch !== "") {
            if (!name.includes(localUserSearch)) {
                return false;
            }
        }

        const matchStartDate = startDateQuery === "" || t.date >= startDateQuery;
        const matchEndDate = endDateQuery === "" || t.date <= endDateQuery;

        return matchStartDate && matchEndDate;
    });

    if (activeTransfers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 20px; color: var(--text-muted);">Không có dữ liệu phù hợp</td></tr>`;
        return;
    }

    const level3Cats = [
        "3.ROOT VEGGIES",
        "3.FRUIT VEGGIES",
        "3.LEAFY VEGGIES",
        "3.PROCESSED VEGGIES",
        "3.HERBS",
        "3.LETTUCE, SNACKABLES",
        "3.MUSHROOM"
    ];
    const dateAgg = {};

    activeTransfers.forEach(t => {
        if (t.nganhHang !== "2.VEGETABLES") {
            return;
        }
        const date = t.date;
        const level3 = t.subCategoryLevel3 || "";

        if (!level3 || !level3Cats.includes(level3)) {
            return;
        }

        if (!dateAgg[date]) {
            dateAgg[date] = {
                date: date,
                categories: {}
            };
            level3Cats.forEach(c => {
                dateAgg[date].categories[c] = { shipped: 0, received: 0, diff: 0 };
            });
        }

        const statusInfo = calculateStatus(t);
        if (statusInfo.statusText === "Đang chuyển") {
            return;
        }

        const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");
        dateAgg[date].categories[level3].shipped += t.qtyShipped;
        dateAgg[date].categories[level3].received += t.qtyReceived + (t.matchedCorrectiveQty || 0);
        if (isDiscrepant) {
            dateAgg[date].categories[level3].diff += Math.abs(statusInfo.chenhLechConLai);
        }
    });

    const sortedDates = Object.keys(dateAgg).sort();

    const getStyleForDailyCat = (rateVal, qtyVal) => {
        if (qtyVal === 0) return "text-align: right;";
        if (rateVal < 0.2) {
            return "background-color: rgba(16, 185, 129, 0.15); color: var(--color-success); font-weight: bold; text-align: right;";
        } else if (rateVal <= 0.5) {
            return "background-color: rgba(245, 158, 11, 0.15); color: var(--color-warning); font-weight: bold; text-align: right;";
        } else {
            return "background-color: rgba(239, 68, 68, 0.15); color: var(--color-danger); font-weight: bold; text-align: right;";
        }
    };

    const localDateSearch = document.getElementById("vegLevel3DateFilterDate") ? document.getElementById("vegLevel3DateFilterDate").value.trim() : "";
    let displayIndex = 1;

    sortedDates.forEach((date) => {
        const formattedDate = formatDateToVN(date);
        if (localDateSearch !== "") {
            if (!formattedDate.includes(localDateSearch)) {
                return;
            }
        }

        const dData = dateAgg[date];
        const tr = document.createElement("tr");

        let htmlContent = `
            <td style="text-align: center;">${displayIndex++}</td>
            <td><strong>${formattedDate}</strong></td>
        `;

        let totalShipped = 0;
        let totalReceived = 0;
        let totalDiff = 0;

        level3Cats.forEach(cat => {
            totalShipped += dData.categories[cat].shipped;
            totalReceived += dData.categories[cat].received;
            totalDiff += dData.categories[cat].diff;
        });

        level3Cats.forEach(cat => {
            const shipped = dData.categories[cat].shipped;
            const diff = dData.categories[cat].diff;
            const rateVal = shipped > 0 ? (diff / shipped) * 100 : 0;
            const style = getStyleForDailyCat(rateVal, shipped);
            const displayText = shipped === 0 ? "0.00%" : `${rateVal.toFixed(2)}%`;
            htmlContent += `<td style="${style}">${displayText}</td>`;
        });

        const totalErrorRate = totalShipped > 0 ? (totalDiff / totalShipped) * 100 : 0;
        const totalStyle = getStyleForDailyCat(totalErrorRate, totalShipped) + " font-weight: bold; border-left: 1px solid var(--border-color);";
        const totalDisplayText = totalShipped === 0 ? "0.00%" : `${totalErrorRate.toFixed(2)}%`;
        htmlContent += `<td style="${totalStyle}">${totalDisplayText}</td>`;

        tr.innerHTML = htmlContent;
        tbody.appendChild(tr);
    });
}

function getPrevDateStr(dateStr) {
    if (!dateStr) return "";
    const parts = dateStr.split("-");
    if (parts.length !== 3) return "";
    const year = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10) - 1; // 0-indexed
    const day = parseInt(parts[2], 10);
    
    const date = new Date(year, month, day);
    date.setDate(date.getDate() - 1);
    
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}

// ============================================================
// Bảng Top 10 SKU chia lệch nhiều nhất theo nhóm ngành hàng
// ============================================================
function renderTopSkuDiscrepancyTable() {
    const tbody = document.getElementById("topSkuDiscrepancyBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    const sortCriteriaEl = document.getElementById("topSkuSortCriteria");
    const sortCriteria = sortCriteriaEl ? sortCriteriaEl.value : "qty";

    const contentCategoryPerformance = document.getElementById("contentCategoryPerformance");
    const isCategoryTabActive = contentCategoryPerformance && contentCategoryPerformance.classList.contains("active");

    const groupSelector = isCategoryTabActive ? "#catFilterGroupContainer input[type='checkbox']:checked" : "#perfFilterGroupContainer input[type='checkbox']:checked";
    const selectedGroups = Array.from(document.querySelectorAll(groupSelector)).map(cb => cb.value);
    
    let activeGroups = [];
    const groupFilterEl = document.getElementById("perfF1GroupFilter");
    const groupFilterVal = groupFilterEl ? groupFilterEl.value : "All";

    if (selectedGroups.length > 0) {
        activeGroups = selectedGroups;
    } else {
        if (groupFilterVal === "All") {
            activeGroups = ["F1", "F2", "HUYHOANG", "CTV"];
        } else {
            activeGroups = [groupFilterVal];
        }
    }

    const tableStartEl = document.getElementById("topSkuStartDate");
    const tableEndEl = document.getElementById("topSkuEndDate");
    const globalStartEl = document.getElementById(isCategoryTabActive ? "catFilterStartDate" : "perfFilterStartDate");
    const globalEndEl = document.getElementById(isCategoryTabActive ? "catFilterEndDate" : "perfFilterEndDate");

    const startDateQuery = (tableStartEl && tableStartEl.value) ? tableStartEl.value : (globalStartEl ? globalStartEl.value : "");
    const endDateQuery = (tableEndEl && tableEndEl.value) ? tableEndEl.value : (globalEndEl ? globalEndEl.value : "");
    
    const prevStartDateQuery = startDateQuery ? getPrevDateStr(startDateQuery) : "";
    const prevEndDateQuery = endDateQuery ? getPrevDateStr(endDateQuery) : "";
    
    const selectedUsers = isCategoryTabActive ? [] : Array.from(document.querySelectorAll("#perfFilterUserContainer input[type='checkbox']:checked")).map(cb => cb.value);
    const localUserSearch = document.getElementById("perfF1UserSearch") ? document.getElementById("perfF1UserSearch").value.toLowerCase().trim() : "";

    const activeTransfers = transfers.filter(t => {
        if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") {
            return false;
        }
        if (!t.nguoiChia) {
            return false;
        }
        const name = t.nguoiChia.trim().toLowerCase();
        
        let matchGroupPrefix = false;
        for (const g of activeGroups) {
            if (name.startsWith(g.toLowerCase())) {
                matchGroupPrefix = true;
                break;
            }
        }
        if (!matchGroupPrefix) return false;

        const matchUser = selectedUsers.length === 0 || selectedUsers.includes(t.nguoiChia);
        if (!matchUser) return false;

        if (localUserSearch !== "") {
            if (!name.includes(localUserSearch)) {
                return false;
            }
        }

        const matchStartDate = startDateQuery === "" || t.date >= startDateQuery;
        const matchEndDate = endDateQuery === "" || t.date <= endDateQuery;

        return matchStartDate && matchEndDate;
    });

    // Filter by SKU Category select dropdown
    const categoryFilterEl = document.getElementById("topSkuCategoryFilter");
    const selectedCategory = categoryFilterEl ? categoryFilterEl.value : "All";

    // Filter by local SKU search box
    const skuSearchEl = document.getElementById("topSkuSearchInput");
    const skuSearchVal = skuSearchEl ? skuSearchEl.value.toLowerCase().trim() : "";

    const skuAgg = {};
    activeTransfers.forEach(t => {
        const cat = t.nganhHang || "Khác";
        
        // Apply Category filter
        if (selectedCategory !== "All" && cat !== selectedCategory) {
            return;
        }

        const itemCode = t.itemCode;
        const itemName = t.itemName || "";
        const unit = t.unit || "";
        
        // Apply local search query
        if (skuSearchVal !== "") {
            if (!itemCode.toLowerCase().includes(skuSearchVal) && !itemName.toLowerCase().includes(skuSearchVal)) {
                return;
            }
        }

        const statusInfo = calculateStatus(t);
        if (statusInfo.statusText === "Đang chuyển") {
            return;
        }

        if (!skuAgg[itemCode]) {
            skuAgg[itemCode] = {
                itemCode: itemCode,
                itemName: itemName,
                unit: unit,
                nganhHang: cat,
                qtyShipped: 0,
                qtyReceived: 0,
                qtyDiff: 0
            };
        }

        skuAgg[itemCode].qtyShipped += t.qtyShipped;
        skuAgg[itemCode].qtyReceived += t.qtyReceived + (t.matchedCorrectiveQty || 0);
        
        const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");
        if (isDiscrepant) {
            skuAgg[itemCode].qtyDiff += Math.abs(statusInfo.chenhLechConLai);
        }
    });

    // Aggregate D-1 transfers
    const prevSkuAgg = {};
    if (prevStartDateQuery && prevEndDateQuery) {
        const prevTransfers = transfers.filter(t => {
            if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") {
                return false;
            }
            if (!t.nguoiChia) {
                return false;
            }
            const name = t.nguoiChia.trim().toLowerCase();
            
            let matchGroupPrefix = false;
            for (const g of activeGroups) {
                if (name.startsWith(g.toLowerCase())) {
                    matchGroupPrefix = true;
                    break;
                }
            }
            if (!matchGroupPrefix) return false;

            const matchUser = selectedUsers.length === 0 || selectedUsers.includes(t.nguoiChia);
            if (!matchUser) return false;

            if (localUserSearch !== "") {
                if (!name.includes(localUserSearch)) {
                    return false;
                }
            }

            const matchStartDate = t.date >= prevStartDateQuery;
            const matchEndDate = t.date <= prevEndDateQuery;

            return matchStartDate && matchEndDate;
        });

        prevTransfers.forEach(t => {
            const cat = t.nganhHang || "Khác";
            if (selectedCategory !== "All" && cat !== selectedCategory) {
                return;
            }

            const itemCode = t.itemCode;
            const statusInfo = calculateStatus(t);
            if (statusInfo.statusText === "Đang chuyển") {
                return;
            }

            if (!prevSkuAgg[itemCode]) {
                prevSkuAgg[itemCode] = {
                    qtyShipped: 0,
                    qtyReceived: 0,
                    qtyDiff: 0
                };
            }

            prevSkuAgg[itemCode].qtyShipped += t.qtyShipped;
            prevSkuAgg[itemCode].qtyReceived += t.qtyReceived + (t.matchedCorrectiveQty || 0);
            
            const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");
            if (isDiscrepant) {
                prevSkuAgg[itemCode].qtyDiff += Math.abs(statusInfo.chenhLechConLai);
            }
        });
    }

    let skuList = Object.values(skuAgg);

    // Sort by selected criteria
    if (sortCriteria === "percent") {
        skuList.sort((a, b) => {
            const aRate = a.qtyShipped > 0 ? (a.qtyDiff / a.qtyShipped) : 0;
            const bRate = b.qtyShipped > 0 ? (b.qtyDiff / b.qtyShipped) : 0;
            const rateCmp = bRate - aRate;
            if (rateCmp !== 0) return rateCmp;
            return b.qtyDiff - a.qtyDiff;
        });
    } else {
        // Sort by absolute discrepancy descending, then by shipped quantity descending
        skuList.sort((a, b) => {
            const diffCmp = b.qtyDiff - a.qtyDiff;
            if (diffCmp !== 0) return diffCmp;
            return b.qtyShipped - a.qtyShipped;
        });
    }

    // Take Top 10
    const top10 = skuList.slice(0, 10);

    if (top10.length === 0) {
        tbody.innerHTML = `<tr><td colspan="11" style="text-align: center; padding: 20px; color: var(--text-muted);">Không có dữ liệu phù hợp</td></tr>`;
        return;
    }

    const getStyleForDailyCat = (rateVal, qtyVal) => {
        if (qtyVal === 0) return "text-align: right;";
        if (rateVal < 0.2) {
            return "background-color: rgba(16, 185, 129, 0.15); color: var(--color-success); font-weight: bold; text-align: right;";
        } else if (rateVal <= 0.5) {
            return "background-color: rgba(245, 158, 11, 0.15); color: var(--color-warning); font-weight: bold; text-align: right;";
        } else {
            return "background-color: rgba(239, 68, 68, 0.15); color: var(--color-danger); font-weight: bold; text-align: right;";
        }
    };

    top10.forEach((item, index) => {
        const shipped = item.qtyShipped;
        const diff = item.qtyDiff;
        const rateVal = shipped > 0 ? (diff / shipped) * 100 : 0;
        const style = getStyleForDailyCat(rateVal, shipped);

        // D-1 comparison calculations
        let prevRateText = "—";
        let prevRateStyle = "text-align: right; color: var(--text-muted);";
        let statusHtml = `<span style="color: var(--text-muted);">—</span>`;

        const prevItem = prevSkuAgg[item.itemCode];
        if (prevItem && prevItem.qtyShipped > 0) {
            const prevShipped = prevItem.qtyShipped;
            const prevDiff = prevItem.qtyDiff;
            const prevRateVal = (prevDiff / prevShipped) * 100;
            prevRateText = prevRateVal.toFixed(2) + "%";
            prevRateStyle = getStyleForDailyCat(prevRateVal, prevShipped);

            const diffRate = rateVal - prevRateVal;
            if (Math.abs(diffRate) < 0.005) {
                statusHtml = `<span style="color: var(--text-muted);">—</span>`;
            } else if (diffRate > 0) {
                statusHtml = `<span style="color: var(--color-danger); font-weight: 600;">▲ +${diffRate.toFixed(2)}%</span>`;
            } else {
                statusHtml = `<span style="color: var(--color-success); font-weight: 600;">▼ ${diffRate.toFixed(2)}%</span>`;
            }
        }

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td style="text-align: center; font-weight: bold; color: ${index < 3 ? 'var(--color-danger)' : 'var(--text-primary)'};">${index + 1}</td>
            <td style="font-family: monospace;">${item.itemCode}</td>
            <td style="font-weight: 500;">${item.itemName}</td>
            <td style="text-align: center;">${item.unit}</td>
            <td>${item.nganhHang}</td>
            <td style="text-align: right; font-weight: 500;">${formatNumber(shipped)}</td>
            <td style="text-align: right; font-weight: 500;">${formatNumber(item.qtyReceived)}</td>
            <td style="text-align: right; color: ${diff > 0 ? 'var(--color-danger)' : 'var(--text-muted)'}; font-weight: bold;">${formatDiffNumber(diff)}</td>
            <td style="${style}">${shipped > 0 ? rateVal.toFixed(2) + "%" : "0.00%"}</td>
            <td style="${prevRateStyle}">${prevRateText}</td>
            <td style="text-align: center; font-size: 13px;">${statusHtml}</td>
        `;
        tbody.appendChild(tr);
    });
}

// ============================================================
// Dữ liệu Xuất Excel / CSV Dạng Cột (Tabular Format)
// ============================================================
function getFilteredExportData(datasetType) {
    const startDate = document.getElementById("exportStartDate") ? document.getElementById("exportStartDate").value : "";
    const endDate = document.getElementById("exportEndDate") ? document.getElementById("exportEndDate").value : "";

    if (datasetType === "transfers") {
        const data = transfers.filter(t => {
            const matchStart = startDate === "" || t.date >= startDate;
            const matchEnd = endDate === "" || t.date <= endDate;
            return matchStart && matchEnd;
        });
        
        const headers = ["Ngày chuyển", "Chi nhánh chuyển", "Chi nhánh nhận", "Người chia", "Mã hàng", "Tên hàng", "Đơn vị tính", "Ngành hàng", "SL chuyển", "SL nhận", "Chênh lệch", "SL bổ sung", "SL chênh lệch còn lại", "Trạng thái"];
        
        const rows = data.map(t => {
            const statusInfo = calculateStatus(t);
            return [
                t.date,
                t.fromBranch,
                t.toBranch,
                t.nguoiChia || "",
                t.itemCode,
                t.itemName,
                t.unit,
                t.nganhHang || "Khác",
                statusInfo.slChuyenKRC,
                statusInfo.slNhanKRC === -1 ? -1 : statusInfo.slNhanKRC,
                statusInfo.slNhanKRC === -1 ? 0 : statusInfo.chenhLech,
                statusInfo.slBoSung,
                statusInfo.slNhanKRC === -1 ? 0 : statusInfo.chenhLechConLai,
                statusInfo.statusText
            ];
        });
        
        return { headers, rows };
    }
    
    if (datasetType === "performance") {
        const data = performanceTransfers.filter(t => {
            const matchStart = startDate === "" || t.ngayChuyen >= startDate;
            const matchEnd = endDate === "" || t.ngayChuyen <= endDate;
            return matchStart && matchEnd;
        });
        
        const headers = ["Ngày chuyển", "Mã Phiếu", "Nơi nhận", "Barcode", "Tên sản phẩm", "Đơn vị", "Ngành hàng", "SL chuyển", "SL nhận", "Chênh lệch", "Bổ sung", "CL còn lại", "Người chia hàng", "Trạng thái"];
        
        const rows = data.map(t => {
            const statusInfo = calculateStatus(t);
            const rawDiff = t.qtyReceived - t.qtyShipped;
            return [
                t.date,
                t.transferCode,
                t.toBranch,
                t.itemCode,
                t.itemName,
                t.unit,
                t.nganhHang || "Khác",
                t.qtyShipped,
                t.qtyReceived,
                rawDiff,
                t.matchedCorrectiveQty || 0,
                statusInfo.chenhLechConLai,
                t.nguoiChia || "",
                getPerfStatus(t)
            ];
        });
        
        return { headers, rows };
    }
    
    if (datasetType === "category") {
        const activeTransfers = transfers.filter(t => {
            if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") return false;
            if (!t.nguoiChia) return false;
            const matchStart = startDate === "" || t.date >= startDate;
            const matchEnd = endDate === "" || t.date <= endDate;
            return matchStart && matchEnd;
        });
        
        const categories = ["2.VEGETABLES", "2.FRUITS", "2.BAKERY", "2.EGGS", "2.DELICA"];
        const userAgg = {};
        
        activeTransfers.forEach(t => {
            const user = t.nguoiChia.trim();
            const cat = t.nganhHang || "Khác";
            
            if (!userAgg[user]) {
                userAgg[user] = {
                    user: user,
                    categories: {}
                };
                categories.forEach(c => {
                    userAgg[user].categories[c] = { shipped: 0, received: 0, diff: 0 };
                });
            }
            
            const statusInfo = calculateStatus(t);
            if (statusInfo.statusText === "Đang chuyển") return;
            
            if (categories.includes(cat)) {
                const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");
                userAgg[user].categories[cat].shipped += t.qtyShipped;
                userAgg[user].categories[cat].received += t.qtyReceived + (t.matchedCorrectiveQty || 0);
                if (isDiscrepant) {
                    userAgg[user].categories[cat].diff += Math.abs(statusInfo.chenhLechConLai);
                }
            }
        });
        
        const headers = ["Nhân sự", "Nhóm nhân sự", "Ngành hàng", "SL chuyển", "SL nhận + Bổ sung", "SL lệch còn lại", "Tỷ lệ chia sai"];
        const rows = [];
        
        Object.keys(userAgg).sort((a,b) => a.localeCompare(b, "vi")).forEach(user => {
            const uData = userAgg[user];
            const name = user.toLowerCase();
            let group = "CTV";
            if (name.startsWith("f1")) group = "F1";
            else if (name.startsWith("f2")) group = "F2";
            else if (name.startsWith("huyhoang")) group = "HUYHOANG";
            
            categories.forEach(cat => {
                const shipped = uData.categories[cat].shipped;
                const received = uData.categories[cat].received;
                const diff = uData.categories[cat].diff;
                if (shipped === 0 && received === 0 && diff === 0) return;
                const rate = shipped > 0 ? (diff / shipped) * 100 : 0;
                rows.push([
                    user,
                    group,
                    cat,
                    shipped,
                    received,
                    diff,
                    `${rate.toFixed(2)}%`
                ]);
            });
        });
        
        return { headers, rows };
    }
    
    if (datasetType === "ctvSummary") {
        const activeTransfers = transfers.filter(t => {
            if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") return false;
            if (!t.nguoiChia) return false;
            
            const matchStart = startDate === "" || t.date >= startDate;
            const matchEnd = endDate === "" || t.date <= endDate;
            return matchStart && matchEnd;
        });
        
        const userAgg = {};
        activeTransfers.forEach(t => {
            const user = t.nguoiChia || "Không rõ";
            if (!userAgg[user]) {
                userAgg[user] = {
                    user: user,
                    storesShared: new Set(),
                    storesDiscrepant: new Set(),
                    totalLines: 0,
                    discrepantLines: 0,
                    diffQtyKg: 0,
                    diffQtyPack: 0,
                    totalReqQty: 0,
                    totalDiffQty: 0,
                    totalSharedQty: 0
                };
            }
            
            const statusInfo = calculateStatus(t);
            if (statusInfo.statusText === "Đang chuyển") return;
            
            const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");
            if (t.toBranch) {
                const branchName = t.toBranch.trim();
                userAgg[user].storesShared.add(branchName);
                if (isDiscrepant) {
                    userAgg[user].storesDiscrepant.add(branchName);
                }
            }
            
            userAgg[user].totalLines += 1;
            userAgg[user].totalReqQty += t.qtyShipped;
            userAgg[user].totalSharedQty += (t.qtyReceived + (t.matchedCorrectiveQty || 0));
            
            if (isDiscrepant) {
                userAgg[user].discrepantLines += 1;
                const absDiff = Math.abs(statusInfo.chenhLechConLai);
                userAgg[user].totalDiffQty += absDiff;
                
                const isKg = (t.unit && t.unit.toLowerCase() === "kg");
                if (isKg) {
                    userAgg[user].diffQtyKg += absDiff;
                } else {
                    userAgg[user].diffQtyPack += absDiff;
                }
            }
        });
        
        const headers = ["Người chia hàng", "Nhóm nhân sự", "Tổng số ST chia", "Tổng số ST lệch", "% ST sai", "Tổng SL chia", "SL chia sai", "% SL chia sai", "SL lệch - Kg", "SL lệch - Pack"];
        const rows = [];
        
        Object.keys(userAgg).sort((a,b) => a.localeCompare(b, "vi")).forEach(user => {
            const item = userAgg[user];
            const name = user.toLowerCase();
            let group = "CTV";
            if (name.startsWith("f1")) group = "F1";
            else if (name.startsWith("f2")) group = "F2";
            else if (name.startsWith("huyhoang")) group = "HUYHOANG";
            
            const stErrorRate = item.storesShared.size > 0 ? ((item.storesDiscrepant.size / item.storesShared.size) * 100).toFixed(2) + "%" : "0.00%";
            const qtyErrorRate = item.totalReqQty > 0 ? ((item.totalDiffQty / item.totalReqQty) * 100).toFixed(2) + "%" : "0.00%";
            
            rows.push([
                user,
                group,
                item.storesShared.size,
                item.storesDiscrepant.size,
                stErrorRate,
                item.totalReqQty,
                item.totalDiffQty,
                qtyErrorRate,
                item.diffQtyKg,
                item.diffQtyPack
            ]);
        });
        
        return { headers, rows };
    }
    
    if (datasetType === "categoryDate") {
        const activeTransfers = transfers.filter(t => {
            if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") return false;
            if (!t.nguoiChia) return false;
            const matchStart = startDate === "" || t.date >= startDate;
            const matchEnd = endDate === "" || t.date <= endDate;
            return matchStart && matchEnd;
        });
        
        const categories = ["2.VEGETABLES", "2.FRUITS", "2.BAKERY", "2.EGGS", "2.DELICA"];
        const dateAgg = {};
        
        activeTransfers.forEach(t => {
            const date = t.date;
            const cat = t.nganhHang || "Khác";
            
            if (!dateAgg[date]) {
                dateAgg[date] = {
                    date: date,
                    categories: {}
                };
                categories.forEach(c => {
                    dateAgg[date].categories[c] = { shipped: 0, received: 0, diff: 0 };
                });
            }
            
            const statusInfo = calculateStatus(t);
            if (statusInfo.statusText === "Đang chuyển") return;
            
            if (categories.includes(cat)) {
                const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");
                dateAgg[date].categories[cat].shipped += t.qtyShipped;
                dateAgg[date].categories[cat].received += t.qtyReceived + (t.matchedCorrectiveQty || 0);
                if (isDiscrepant) {
                    dateAgg[date].categories[cat].diff += Math.abs(statusInfo.chenhLechConLai);
                }
            }
        });
        
        const headers = ["Ngày", "Ngành hàng", "SL chuyển", "SL nhận + Bổ sung", "SL lệch còn lại", "Tỷ lệ chia sai"];
        const rows = [];
        
        Object.keys(dateAgg).sort().forEach(date => {
            const dData = dateAgg[date];
            categories.forEach(cat => {
                const shipped = dData.categories[cat].shipped;
                const received = dData.categories[cat].received;
                const diff = dData.categories[cat].diff;
                const rate = shipped > 0 ? (diff / shipped) * 100 : 0;
                rows.push([
                    date,
                    cat,
                    shipped,
                    received,
                    diff,
                    `${rate.toFixed(2)}%`
                ]);
            });
        });
        
        return { headers, rows };
    }
    
    return { headers: [], rows: [] };
}

function renderExportPreview() {
    const datasetSelect = document.getElementById("exportDatasetSelect");
    if (!datasetSelect) return;
    
    const datasetType = datasetSelect.value;
    const { headers, rows } = getFilteredExportData(datasetType);
    
    // Update count
    const countEl = document.getElementById("exportRecordCount");
    if (countEl) {
        countEl.innerText = `Sẵn sàng xuất ${formatNumber(rows.length)} dòng dữ liệu.`;
    }
    
    // Render head
    const thead = document.getElementById("exportPreviewHead");
    if (thead) {
        thead.innerHTML = `<tr>${headers.map(h => `<th>${h}</th>`).join("")}</tr>`;
    }
    
    // Render preview body (first 10 rows)
    const tbody = document.getElementById("exportPreviewBody");
    if (tbody) {
        tbody.innerHTML = "";
        const previewRows = rows.slice(0, 10);
        if (previewRows.length === 0) {
            tbody.innerHTML = `<tr><td colspan="${headers.length || 1}" style="text-align: center; padding: 20px; color: var(--text-muted);">Không có dữ liệu phù hợp</td></tr>`;
            return;
        }
        
        previewRows.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = row.map(val => {
                const isNumeric = typeof val === "number";
                const alignStyle = isNumeric ? 'style="text-align: right;"' : '';
                const displayVal = isNumeric ? formatNumber(val) : val;
                return `<td ${alignStyle}>${displayVal}</td>`;
            }).join("");
            tbody.appendChild(tr);
        });
    }
}

function downloadExportDataset() {
    const datasetSelect = document.getElementById("exportDatasetSelect");
    if (!datasetSelect) return;
    
    const datasetType = datasetSelect.value;
    const { headers, rows } = getFilteredExportData(datasetType);
    
    if (rows.length === 0) {
        alert("Không có dữ liệu để xuất!");
        return;
    }
    
    let csvContent = "\uFEFF"; // UTF-8 BOM representation
    csvContent += headers.join(",") + "\n";
    
    rows.forEach(row => {
        const formattedRow = row.map(val => {
            if (typeof val === "string") {
                return `"${val.replace(/"/g, '""')}"`;
            }
            return val;
        });
        csvContent += formattedRow.join(",") + "\n";
    });
    
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    
    const todayStr = new Date().toISOString().split("T")[0];
    let filename = `BaoCao_Tabular_${datasetType}_${todayStr}.csv`;
    if (datasetType === "transfers") filename = `BaoCao_DieuChuyenHang_Col_${todayStr}.csv`;
    else if (datasetType === "performance") filename = `BaoCao_HieuSuatChiaHang_Col_${todayStr}.csv`;
    else if (datasetType === "category") filename = `BaoCao_HieuSuatNganhHang_Col_${todayStr}.csv`;
    else if (datasetType === "ctvSummary") filename = `BaoCao_TomTatHieuSuat_Col_${todayStr}.csv`;
    else if (datasetType === "categoryDate") filename = `BaoCao_HieuSuatNganhHangTheoNgay_Col_${todayStr}.csv`;
    
    link.setAttribute("download", filename);
    link.style.visibility = "hidden";
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Helper function to export any DOM table directly to CSV
function downloadTableToExcel(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = [];
    const trs = table.querySelectorAll("tr");
    
    trs.forEach(tr => {
        if (tr.style.display === "none") return;
        
        const row = [];
        const cells = tr.querySelectorAll("th, td");
        cells.forEach(cell => {
            let text = cell.innerText.trim().replace(/\n/g, " ");
            
            const select = cell.querySelector("select");
            if (select) {
                const span = cell.querySelector("span");
                text = span ? span.innerText.trim() : select.options[select.selectedIndex].text;
            }
            row.push(text);
        });
        rows.push(row);
    });
    
    if (rows.length === 0) {
        alert("Không có dữ liệu để xuất!");
        return;
    }
    
    let csvContent = "\uFEFF"; // UTF-8 BOM
    rows.forEach(row => {
        const formattedRow = row.map(val => {
            return `"${val.replace(/"/g, '""')}"`;
        });
        csvContent += formattedRow.join(",") + "\n";
    });
    
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.style.visibility = "hidden";
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Helper to export clean raw tabular data directly to CSV file
function downloadCSV(headers, rows, filename) {
    let csvContent = "\uFEFF"; // UTF-8 BOM representation
    csvContent += headers.join(",") + "\n";
    
    rows.forEach(row => {
        const formattedRow = row.map(val => {
            if (typeof val === "string") {
                return `"${val.replace(/"/g, '""')}"`;
            }
            return val;
        });
        csvContent += formattedRow.join(",") + "\n";
    });
    
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.style.visibility = "hidden";
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Export Category Performance by divided personnel in row-by-row (tabular) format
function downloadCategoryF1Tabular() {
    const catGroupEl = document.getElementById("catFilterGroupContainer");
    const groupSelector = catGroupEl ? "#catFilterGroupContainer input[type='checkbox']:checked" : "#perfFilterGroupContainer input[type='checkbox']:checked";
    const selectedGroups = Array.from(document.querySelectorAll(groupSelector)).map(cb => cb.value);
    
    let activeGroups = [];
    const groupFilterEl = document.getElementById("perfF1GroupFilter");
    const groupFilterVal = groupFilterEl ? groupFilterEl.value : "All";

    if (selectedGroups.length > 0) {
        activeGroups = selectedGroups;
    } else {
        if (groupFilterVal === "All") {
            activeGroups = ["F1", "F2", "HUYHOANG", "CTV"];
        } else {
            activeGroups = [groupFilterVal];
        }
    }

    const catStartEl = document.getElementById("catFilterStartDate");
    const catEndEl = document.getElementById("catFilterEndDate");
    const startDateQuery = catStartEl ? catStartEl.value : (document.getElementById("perfFilterStartDate") ? document.getElementById("perfFilterStartDate").value : "");
    const endDateQuery = catEndEl ? catEndEl.value : (document.getElementById("perfFilterEndDate") ? document.getElementById("perfFilterEndDate").value : "");
    
    const localUserSearch = document.getElementById("perfF1UserSearch") ? document.getElementById("perfF1UserSearch").value.toLowerCase().trim() : "";

    const activeTransfers = transfers.filter(t => {
        if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") return false;
        if (!t.nguoiChia) return false;
        const name = t.nguoiChia.trim().toLowerCase();
        
        let matchGroupPrefix = false;
        for (const g of activeGroups) {
            if (name.startsWith(g.toLowerCase())) {
                matchGroupPrefix = true;
                break;
            }
        }
        if (!matchGroupPrefix) return false;

        if (localUserSearch !== "") {
            if (!name.includes(localUserSearch)) return false;
        }

        const matchStartDate = startDateQuery === "" || t.date >= startDateQuery;
        const matchEndDate = endDateQuery === "" || t.date <= endDateQuery;
        return matchStartDate && matchEndDate;
    });

    if (activeTransfers.length === 0) {
        alert("Không có dữ liệu để xuất!");
        return;
    }

    const categories = ["2.VEGETABLES", "2.FRUITS", "2.BAKERY", "2.EGGS", "2.DELICA"];
    const userAgg = {};
    
    activeTransfers.forEach(t => {
        const user = t.nguoiChia.trim();
        const cat = t.nganhHang || "Khác";
        
        if (!userAgg[user]) {
            userAgg[user] = {
                user: user,
                categories: {}
            };
            categories.forEach(c => {
                userAgg[user].categories[c] = { shipped: 0, received: 0, diff: 0 };
            });
        }
        
        const statusInfo = calculateStatus(t);
        if (statusInfo.statusText === "Đang chuyển") return;
        
        if (categories.includes(cat)) {
            const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");
            userAgg[user].categories[cat].shipped += t.qtyShipped;
            userAgg[user].categories[cat].received += t.qtyReceived + (t.matchedCorrectiveQty || 0);
            if (isDiscrepant) {
                userAgg[user].categories[cat].diff += Math.abs(statusInfo.chenhLechConLai);
            }
        }
    });

    const headers = ["Nhân sự", "Nhóm nhân sự", "Ngành hàng", "SL chuyển", "SL nhận + Bổ sung", "SL lệch còn lại", "Tỷ lệ chia sai"];
    const rows = [];
    
    Object.keys(userAgg).sort((a,b) => a.localeCompare(b, "vi")).forEach(user => {
        const uData = userAgg[user];
        const name = user.toLowerCase();
        let group = "CTV";
        if (name.startsWith("f1")) group = "F1";
        else if (name.startsWith("f2")) group = "F2";
        else if (name.startsWith("huyhoang")) group = "HUYHOANG";
        
        categories.forEach(cat => {
            const shipped = uData.categories[cat].shipped;
            const received = uData.categories[cat].received;
            const diff = uData.categories[cat].diff;
            if (shipped === 0 && received === 0 && diff === 0) return;
            const rate = shipped > 0 ? (diff / shipped) * 100 : 0;
            rows.push([
                user,
                group,
                cat,
                shipped,
                received,
                diff,
                `${rate.toFixed(2)}%`
            ]);
        });
    });

    downloadCSV(headers, rows, `BaoCao_HieuSuatNganhHang_Dong_NhanSu_${new Date().toISOString().split("T")[0]}.csv`);
}

// Export Category Performance by date in row-by-row (tabular) format
function downloadCategoryDateTabular() {
    const catGroupEl = document.getElementById("catFilterGroupContainer");
    const groupSelector = catGroupEl ? "#catFilterGroupContainer input[type='checkbox']:checked" : "#perfFilterGroupContainer input[type='checkbox']:checked";
    const selectedGroups = Array.from(document.querySelectorAll(groupSelector)).map(cb => cb.value);
    
    let activeGroups = [];
    const groupFilterEl = document.getElementById("perfF1GroupFilter");
    const groupFilterVal = groupFilterEl ? groupFilterEl.value : "All";

    if (selectedGroups.length > 0) {
        activeGroups = selectedGroups;
    } else {
        if (groupFilterVal === "All") {
            activeGroups = ["F1", "F2", "HUYHOANG", "CTV"];
        } else {
            activeGroups = [groupFilterVal];
        }
    }

    const catStartEl = document.getElementById("catFilterStartDate");
    const catEndEl = document.getElementById("catFilterEndDate");
    const startDateQuery = catStartEl ? catStartEl.value : (document.getElementById("perfFilterStartDate") ? document.getElementById("perfFilterStartDate").value : "");
    const endDateQuery = catEndEl ? catEndEl.value : (document.getElementById("perfFilterEndDate") ? document.getElementById("perfFilterEndDate").value : "");
    
    const localDateSearch = document.getElementById("catDateTableFilterDate") ? document.getElementById("catDateTableFilterDate").value.trim() : "";

    const activeTransfers = transfers.filter(t => {
        if ((t.fromBranch || "").toString().normalize("NFC").trim().toLowerCase() !== "kho rau củ") return false;
        if (!t.nguoiChia) return false;
        const name = t.nguoiChia.trim().toLowerCase();
        
        let matchGroupPrefix = false;
        for (const g of activeGroups) {
            if (name.startsWith(g.toLowerCase())) {
                matchGroupPrefix = true;
                break;
            }
        }
        if (!matchGroupPrefix) return false;

        const matchStartDate = startDateQuery === "" || t.date >= startDateQuery;
        const matchEndDate = endDateQuery === "" || t.date <= endDateQuery;
        return matchStartDate && matchEndDate;
    });

    if (activeTransfers.length === 0) {
        alert("Không có dữ liệu để xuất!");
        return;
    }

    const categories = ["2.VEGETABLES", "2.FRUITS", "2.BAKERY", "2.EGGS", "2.DELICA"];
    const dateAgg = {};
    
    activeTransfers.forEach(t => {
        const date = t.date;
        const cat = t.nganhHang || "Khác";
        
        if (!dateAgg[date]) {
            dateAgg[date] = {
                date: date,
                categories: {}
            };
            categories.forEach(c => {
                dateAgg[date].categories[c] = { shipped: 0, received: 0, diff: 0 };
            });
        }
        
        const statusInfo = calculateStatus(t);
        if (statusInfo.statusText === "Đang chuyển") return;
        
        if (categories.includes(cat)) {
            const isDiscrepant = (statusInfo.statusText === "Thiếu" || statusInfo.statusText === "Dư");
            dateAgg[date].categories[cat].shipped += t.qtyShipped;
            dateAgg[date].categories[cat].received += t.qtyReceived + (t.matchedCorrectiveQty || 0);
            if (isDiscrepant) {
                dateAgg[date].categories[cat].diff += Math.abs(statusInfo.chenhLechConLai);
            }
        }
    });

    const headers = ["Ngày", "Ngành hàng", "SL chuyển", "SL nhận + Bổ sung", "SL lệch còn lại", "Tỷ lệ chia sai"];
    const rows = [];
    
    Object.keys(dateAgg).sort().forEach(date => {
        const dData = dateAgg[date];
        const formattedDate = formatDateToVN(date);
        
        if (localDateSearch !== "") {
            if (!formattedDate.includes(localDateSearch)) {
                return;
            }
        }
        
        categories.forEach(cat => {
            const shipped = dData.categories[cat].shipped;
            const received = dData.categories[cat].received;
            const diff = dData.categories[cat].diff;
            if (shipped === 0 && received === 0 && diff === 0) return;
            const rate = shipped > 0 ? (diff / shipped) * 100 : 0;
            rows.push([
                formattedDate,
                cat,
                shipped,
                received,
                diff,
                `${rate.toFixed(2)}%`
            ]);
        });
    });

    if (rows.length === 0) {
        alert("Không có dữ liệu để xuất!");
        return;
    }

    downloadCSV(headers, rows, `BaoCao_HieuSuatNganhHang_Dong_Ngay_${new Date().toISOString().split("T")[0]}.csv`);
}
