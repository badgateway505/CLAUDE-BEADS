# Bead 03-02: Add User Login Endpoint

<meta>
```yaml
id: 03-02-user-login
phase: 03-authentication
model: sonnet
cost_estimate: 0.25 USD
verification_tier: AUTO
verification_cmd: "pytest tests/test_auth.py::test_login -v"
depends_on: ["03-01"]
```
</meta>

---

<intent>
**Goal**: Implement POST /auth/login endpoint with JWT token generation

**Success Criteria**:
- [ ] Endpoint accepts username/password
- [ ] Returns JWT token on valid credentials
- [ ] Returns 401 on invalid credentials
- [ ] Unit tests pass
</intent>

---

<tasks>
### 1. Create login endpoint
- **What**: Add POST /auth/login route handler
- **Verify**: `curl -X POST http://localhost:8000/auth/login`

### 2. Add tests
- **What**: Write test_login_success and test_login_invalid
- **Verify**: `pytest tests/test_auth.py -v`

### 3. Commit
- **Message**: `feat(03-02): add user login endpoint`
</tasks>

---

<verification>
**Tier**: AUTO

**Command**:
```bash
pytest tests/test_auth.py::test_login -v
```

**Expected**: All tests pass (2/2 green)

**On Failure**:
| Symptom | Fix |
|---------|-----|
| ImportError | Run `pip install -e .` |
| 401 expected, got 200 | Check password validation logic |
</verification>
