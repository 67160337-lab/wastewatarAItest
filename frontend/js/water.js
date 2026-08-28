requireLogin();

// 1. ฟังก์ชันดึงประวัติการบันทึกคุณภาพน้ำมาแสดงในตาราง
async function loadWaterHistory() {
  const tbody = document.getElementById("waterHistoryBody");
  if (!tbody) return; // ป้องกัน error ถ้าหา element ไม่เจอ

  try {
    const historyData = await api("/water", { method: "GET" });
    tbody.innerHTML = ""; // ล้างข้อมูลเก่าก่อน

    if (!historyData || historyData.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;">ยังไม่มีประวัติการบันทึก</td></tr>`;
      return;
    }

    historyData.forEach(item => {
      const dateObj = new Date(item.created_at);
      const dateStr = isNaN(dateObj) ? item.created_at : dateObj.toLocaleString("th-TH");

      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${dateStr}</td>
        <td>${item.influent_cod}</td>
        <td>${item.flow_rate}</td>
        <td>${item.water_temp}</td>
        <td>${item.current_do}</td>
        <td><span class="badge">${item.status}</span></td>
      `;
      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Error loading water history:", err);
  }
}

// 2. เรียกโหลดประวัติทันทีเมื่อเปิดหน้าเว็บ
document.addEventListener("DOMContentLoaded", loadWaterHistory);

// 3. ฟอร์มบันทึกข้อมูลเดิม (เพิ่มการสั่งโหลดประวัติใหม่หลังบันทึก)
document.getElementById("waterForm").addEventListener("submit", async e => {
  e.preventDefault();
  const message = document.getElementById("message");
  try {
    const data = await api("/water", {
      method: "POST",
      body: JSON.stringify({
        influent_cod: +cod.value,
        flow_rate: +flow.value,
        water_temp: +temp.value,
        current_do: +document.getElementById("do").value
      })
    });
    message.textContent = "Saved: " + data.status;
    e.target.reset();
    
    // เรียกดึงประวัติใหม่ทันทีหลังจากบันทึกสำเร็จ
    loadWaterHistory();
  } catch(err) { 
    message.textContent = err.message; 
  }
});