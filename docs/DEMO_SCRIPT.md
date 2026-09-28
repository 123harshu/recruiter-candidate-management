##### `docs/DEMO_SCRIPT.md`
```markdown
# Technical Assessment Demonstration Script

## 0:00 - Introduction & Setup
* **What to say:** "I will demonstrate the Recruiter Candidate Management application. Setup on Windows requires executing `setup.bat` and `run.bat`."
* **What to show:** Open terminal, run `setup.bat`, then `run.bat`.

## 1:30 - Dashboard & Candidate Creation
* **What to click:** Click `+ Add Candidate` button.
* **What to show:** Form submission for "Harshita Verma".
* **What to say:** "New candidates enter directly into the Applied stage, and an initial audit trail record is generated."

## 3:00 - Search & Filtering
* **What to show:**
  1. Type `Harsh` in search box (demonstrates RapidFuzz matching).
  2. Select `Interview` stage filter.
  3. Enter `Min Days in Stage = 5` (shows Candidate A with 8 days, excluding Candidate B with 2 days).

## 4:30 - Stage Transition & Immutability Audit
* **What to click:** Open candidate details page for "Harshita Verma".
* **What to show:** View the complete timeline. Advance candidate through `Move to Next`.
* **What to say:** "The history log is strictly append-only. Transitions are managed within atomic database transactions."