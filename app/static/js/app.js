const NEXT_STAGES = {
  "Applied": "Screening",
  "Screening": "Interview",
  "Interview": "Offer",
  "Offer": "Hired"
};

function showToast(message, isError = false) {
  const container = document.getElementById("toast-container");
  if (!container) return;
  
  const toast = document.createElement("div");
  toast.className = `toast ${isError ? "toast-error" : "toast-success"}`;
  toast.innerText = message;
  
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

async function advanceCandidate(candidateId, currentStage) {
  const targetStage = NEXT_STAGES[currentStage];
  if (!targetStage) return;

  const reason = prompt(`Advancing to '${targetStage}'. Reason:`, `Passed ${currentStage} evaluation`);
  if (reason === null) return; // User cancelled prompt

  try {
    const res = await fetch(`/api/candidates/${candidateId}/stage`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        stage: targetStage,
        changed_by: "Recruiter Admin",
        reason: reason || "Advanced by recruiter"
      })
    });

    const data = await res.json();
    if (!res.ok) {
      const errMsg = data.detail?.message || data.detail || "Stage update failed";
      showToast(errMsg, true);
      return;
    }

    showToast(`Successfully moved candidate to ${targetStage}!`);
    setTimeout(() => window.location.reload(), 600);
  } catch (err) {
    showToast("Network error occurred during stage transition.", true);
  }
}

async function applyFilters() {
  const search = document.getElementById("search-input").value;
  const stage = document.getElementById("stage-select").value;
  const minDays = document.getElementById("min-days").value;
  const maxDays = document.getElementById("max-days").value;

  const params = new URLSearchParams();
  if (search) params.append("search", search);
  if (stage) params.append("stage", stage);
  if (minDays) params.append("min_days_in_stage", minDays);
  if (maxDays) params.append("max_days_in_stage", maxDays);

  try {
    const res = await fetch(`/api/candidates?${params.toString()}`);
    if (!res.ok) throw new Error("Failed to search candidates");
    const candidates = await res.json();

    renderFilteredBoard(candidates);
    showToast(`Found ${candidates.length} matching candidate(s)`);
  } catch (err) {
    showToast(err.message, true);
  }
}

function resetFilters() {
  document.getElementById("search-input").value = "";
  document.getElementById("stage-select").value = "";
  document.getElementById("min-days").value = "";
  document.getElementById("max-days").value = "";
  applyFilters();
}

function renderFilteredBoard(candidates) {
  const stages = ["Applied", "Screening", "Interview", "Offer", "Hired"];
  
  stages.forEach(st => {
    const colList = document.getElementById(`list-${st.toLowerCase()}`);
    const badge = document.getElementById(`count-${st.toLowerCase()}`);
    if (!colList) return;

    const stageCandidates = candidates.filter(c => c.current_stage === st);
    if (badge) badge.innerText = stageCandidates.length;

    if (stageCandidates.length === 0) {
      colList.innerHTML = `<p class="empty-state">No candidates in ${st}</p>`;
      return;
    }

    colList.innerHTML = stageCandidates.map(c => `
      <div class="candidate-card" id="card-${c.id}">
        <div class="card-title-row">
          <h4 class="candidate-name">${escapeHtml(c.full_name)}</h4>
          <span class="age-badge">${c.days_in_current_stage}d in stage</span>
        </div>
        <p class="candidate-pos"><strong>Position:</strong> ${escapeHtml(c.position)}</p>
        <p class="candidate-email"><strong>Email:</strong> ${escapeHtml(c.email)}</p>
        <p class="candidate-source"><small>Source: ${escapeHtml(c.source || "Direct")}</small></p>
        <div class="card-footer">
          <a href="/candidates/${c.id}" class="btn-link">View Details</a>
          ${st !== "Hired" ? `
            <button class="btn btn-sm btn-action" onclick="advanceCandidate(${c.id}, '${st}')">
              Move to Next &rarr;
            </button>
          ` : ''}
        </div>
      </div>
    `).join('');
  });
}

async function submitCandidateForm(event) {
  event.preventDefault();
  const payload = {
    full_name: document.getElementById("full_name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value || null,
    position: document.getElementById("position").value,
    source: document.getElementById("source").value
  };

  try {
    const res = await fetch("/api/candidates", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      showToast(data.detail || "Error creating candidate", true);
      return;
    }

    showToast("Candidate created successfully!");
    setTimeout(() => { window.location.href = "/"; }, 800);
  } catch (err) {
    showToast("Server communication error", true);
  }
}

function escapeHtml(str) {
  return String(str || '').replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}