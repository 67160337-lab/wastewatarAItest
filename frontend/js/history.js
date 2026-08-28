requireLogin();
async function loadHistory(){
  const body = document.getElementById("history");
  try {
    const rows = await api("/predictions");
    body.innerHTML = rows.map(r => `
      <tr>
        <td>${new Date(r.created_at).toLocaleString()}</td>
        <td>${r.influent_cod}</td>
        <td>${r.flow_rate}</td>
        <td>${r.water_temp}</td>
        <td>${r.current_do}</td>
        <td><b>${r.predicted_speed}%</b></td>
      </tr>
    `).join("") || '<tr><td colspan="6">No prediction records</td></tr>';
  } catch(err) { body.innerHTML = `<tr><td colspan="6">${err.message}</td></tr>`; }
}
loadHistory();
