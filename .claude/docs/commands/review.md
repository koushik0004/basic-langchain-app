# Review

Review $FILE for issues. Output format:

ISSUES (bullet, severity: high/med/low):
- [high] ...

QUICK FIXES (code only, no prose):
```python
# fix for issue 1
```

SKIP: style issues, minor naming, anything not affecting correctness or perf.
Stop after listing. Do not auto-apply fixes.
