# Bead 05-03: Dashboard Chart Rendering

<meta>
```yaml
id: 05-03-dashboard-charts
phase: 05-frontend-ui
model: sonnet
cost_estimate: 0.30 USD
verification_tier: MANUAL
verification_checklist:
  - [ ] Dashboard loads without errors in browser console
  - [ ] Line chart displays with correct data points
  - [ ] Chart legend shows all series names
  - [ ] Responsive - chart resizes on window resize
rationale: "Visual verification - automated screenshot testing not yet implemented"
depends_on: ["05-01", "05-02"]
```
</meta>

---

<intent>
**Goal**: Implement interactive charts on admin dashboard using Chart.js

**Success Criteria**:
- [ ] Chart renders on /dashboard page
- [ ] Data fetched from API correctly
- [ ] Visual appearance matches design
- [ ] Manual checklist verified
</intent>

---

<tasks>
### 1. Add Chart.js component
- **What**: Create LineChart component, fetch data from /api/metrics
- **Verify**: Check browser console for errors

### 2. Style and integrate
- **What**: Add chart to dashboard.html, apply CSS styling
- **Verify**: Open http://localhost:3000/dashboard

### 3. Commit
- **Message**: `feat(05-03): add dashboard charts`
</tasks>

---

<verification>
**Tier**: MANUAL

**Checklist**:
- [ ] **Page loads**: Navigate to http://localhost:3000/dashboard - no errors
- [ ] **Chart renders**: Line chart visible with data points
- [ ] **Legend correct**: Shows "Users", "Revenue", "Signups" series
- [ ] **Responsive**: Resize browser - chart adapts to width

**How to Verify**:
1. Start dev server: `npm run dev`
2. Open http://localhost:3000/dashboard in browser
3. Check each item visually
4. Take screenshot or confirm in session notes
</verification>
