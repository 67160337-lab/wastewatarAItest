requireLogin();

async function loadDashboard(){
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  document.getElementById("username").textContent = user.username || "User";
  try {
    const history = await api("/predictions");
    if (history.length) {
      const r = history[0];
      document.getElementById("doValue").textContent = r.current_do;
      document.getElementById("tempValue").textContent = r.water_temp;
      document.getElementById("codValue").textContent = r.influent_cod;
      document.getElementById("speedValue").textContent = r.predicted_speed;
      document.getElementById("gaugeValue").textContent = r.predicted_speed + "%";
    }
  } catch(e) { console.error(e); }
}
loadDashboard();
