# Research Schema Template (Claude Beads)

**PROTOCOL**: Narrative fluff is prohibited. Use only technical specifications anchored in XML tags.

---

## <research_meta>
```yaml
topic: [Concise topic identifier]
model: [claude-opus-4-5 | claude-sonnet-4-5 | claude-haiku]
date: YYYY-MM-DD
phase: [XX-phase-name]
```
</research_meta>

---

## <objective>
[Single sentence: What technical question must be answered?]
</objective>

---

## <constraints>
```yaml
performance:
  - [Specific metric: value + units]
  - [Latency requirement: value + tolerance]

compatibility:
  - [Platform: version constraint]
  - [Dependency: version + rationale]

resource:
  - [Memory: limit + justification]
  - [CPU/Cores: allocation strategy]

network:
  - [Protocol: constraint + reason]
  - [Bandwidth: requirement]
```
</constraints>

---

## <hardware_spec>
**Required only for embedded/physical systems. Omit if pure software.**

```yaml
platform:
  name: [Device name]
  cpu: [Architecture + clock speed]
  memory: [RAM + type]
  storage: [Flash/disk + speed class]

peripherals:
  - name: [Component identifier]
    interface: [I2S | SPI | UART | GPIO]
    spec: [Datasheet reference or key params]
    constraint: [Critical limitation]

power:
  - [Supply voltage + tolerance]
  - [Current budget: avg/peak]
```
</hardware_spec>

---

## <pattern>
### [Pattern Name]

**Context**: [When/why this pattern applies]

**Structure**:
```
[ASCII diagram, code skeleton, or architectural schematic]
```

**Tradeoffs**:
| Dimension | Impact | Mitigation |
|-----------|--------|------------|
| [Latency] | [Quantified effect] | [Specific remedy] |
| [Memory] | [Quantified effect] | [Specific remedy] |

**Verification**:
```bash
[Command that proves pattern works]
```

---

</pattern>

---

## <alternatives>
### Option A: [Name]
- **Tradeoff**: [Primary concern]
- **Benefit**: [Primary advantage]
- **Verify**: `[command]`

### Option B: [Name]
- **Tradeoff**: [Primary concern]
- **Benefit**: [Primary advantage]
- **Verify**: `[command]`

**Recommendation**: [A|B] — [One-sentence technical justification]
</alternatives>

---

## <verify_cmd>
```bash
# Command that validates research findings
[Exact shell command with expected output pattern]
```
</verify_cmd>

---

## <references>
- [Library/Tool]: [Version] — [Specific feature used]
- [Documentation URL] — [Relevant section]
- [Prior art reference] — [Key insight]
</references>

---

## USAGE RULES

1. **Delete unused sections** — If no hardware, delete `<hardware_spec>`. If no alternatives, delete `<alternatives>`.
2. **No prose** — Bullet points, tables, YAML, code blocks only.
3. **Quantify everything** — "Fast" is meaningless. "< 50ms p99" is actionable.
4. **One research file per technical question** — Don't mix audio codec research with network protocol research.
5. **Verification-first** — Every claim must have a `verify_cmd` or reference.

---

## ANTI-PATTERNS (Forbidden)

❌ "This is a complex problem requiring careful consideration..."
✅ `<constraint>latency: < 100ms p95</constraint>`

❌ "We could potentially explore several approaches..."
✅ `<alternatives>` block with 2-3 concrete options + tradeoff table

❌ "The system should be fast and reliable..."
✅ `<pattern>` block with latency budget + failure mode table
