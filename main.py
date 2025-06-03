import streamlit as st

# HTML & JavaScript code
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>CRA Filing Deadline Calculator (First Nations)</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 30px;
      background: #f4f4f4;
      color: #333;
    }
    h1 {
      color: #004080;
    }
    label {
      font-weight: bold;
      margin-top: 10px;
      display: block;
    }
    select, input[type="date"] {
      padding: 5px;
      margin-bottom: 15px;
      width: 250px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
      background: white;
    }
    table, th, td {
      border: 1px solid #ccc;
    }
    th, td {
      padding: 10px;
      text-align: center;
    }
    button {
      padding: 10px 15px;
      background: #0078d4;
      color: white;
      border: none;
      margin-top: 15px;
      cursor: pointer;
    }
    button:hover {
      background: #005fa3;
    }
  </style>
</head>
<body>
  <h1>CRA Filing Deadline Calculator</h1>

  <label for="filingCode">Filing Code:</label>
  <select id="filingCode">
    <option value="PSB">PSB</option>
    <option value="1A">Code 1A</option>
    <option value="8">Code 8</option>
  </select>

  <label for="filerStatus">Filer Status:</label>
  <select id="filerStatus">
    <option value="filer">Filer</option>
    <option value="non-filer">Non-Filer</option>
  </select>

  <label for="frequency">Filing Frequency:</label>
  <select id="frequency">
    <option value="monthly">Monthly</option>
    <option value="quarterly">Quarterly</option>
    <option value="annually">Annually</option>
  </select>

  <label for="fiscalStart">Fiscal Year Start Date:</label>
  <input type="date" id="fiscalStart" value="2025-04-01" />

  <label for="startYear">Starting Year:</label>
  <select id="startYear">
    <option value="2024">2024</option>
    <option value="2025" selected>2025</option>
    <option value="2026">2026</option>
  </select>

  <br/>
  <button onclick="calculateDeadlines()">Calculate Deadlines</button>

  <table id="resultsTable" style="display:none;">
    <thead>
      <tr>
        <th>Period Start</th>
        <th>Period End</th>
        <th>Filing Deadline</th>
        <th>Latest Allowed Filing Date</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>

  <script>
    function addMonths(date, months) {
      const d = new Date(date);
      d.setMonth(d.getMonth() + months);
      return d;
    }

    function formatDate(date) {
      return date.toISOString().split('T')[0];
    }

    function calculateDeadlines() {
      const frequency = document.getElementById("frequency").value;
      const fiscalStart = new Date(document.getElementById("fiscalStart").value);
      const startYear = parseInt(document.getElementById("startYear").value);
      const filerStatus = document.getElementById("filerStatus").value;

      const table = document.getElementById("resultsTable");
      const tbody = table.querySelector("tbody");
      tbody.innerHTML = "";

      let periods = [];
      let count = frequency === "monthly" ? 12 : frequency === "quarterly" ? 4 : 1;
      let currentStart = new Date(fiscalStart);
      currentStart.setFullYear(startYear);

      for (let i = 0; i < count; i++) {
        let start = new Date(currentStart);
        let end;

        if (frequency === "monthly") {
          end = addMonths(start, 1);
          end.setDate(end.getDate() - 1);
        } else if (frequency === "quarterly") {
          end = addMonths(start, 3);
          end.setDate(end.getDate() - 1);
        } else {
          end = new Date(start);
          end.setFullYear(end.getFullYear() + 1);
          end.setDate(end.getDate() - 1);
        }

        let deadline = new Date(end);
        deadline.setMonth(deadline.getMonth() + 3);

        periods.push({
          periodStart: formatDate(start),
          periodEnd: formatDate(end),
          deadline: formatDate(deadline),
          latest: formatDate(deadline) // Can extend logic for late filing rules if needed
        });

        currentStart = new Date(end);
        currentStart.setDate(currentStart.getDate() + 1);
      }

      periods.forEach(p => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${p.periodStart}</td>
          <td>${p.periodEnd}</td>
          <td>${p.deadline}</td>
          <td>${p.latest}</td>
        `;
        tbody.appendChild(row);
      });

      table.style.display = "table";
    }
  </script>
</body>
</html>
"""

# Set up the Streamlit app
st.title("CRA Filing Deadline Calculator")

# Display HTML & JS using markdown
st.markdown(html_code, unsafe_allow_html=True)

