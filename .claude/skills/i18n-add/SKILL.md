# i18n Add Key

Add a new translation key across all locale files with proper formatting and validation.

## Parameters
- `key`: the new translation key name (e.g., `exportBookingDate`)
- `value`: English default value (e.g., `"Export Booking Date"`)
- `after`: anchor key name to insert after (e.g., `exportBookingNo`)

## Process
1. **Check for duplicates**: Grep all locale files to confirm key does NOT already exist across any locale.
2. **Identify insertion point**: Locate the anchor key in all locale files (e.g., `exportBookingNo`).
3. **Insert in all locales**:
   - Insert new key immediately after the anchor key in every locale file.
   - Preserve exact indentation and formatting — no blank lines before/after.
   - For English locale: use the provided `value`.
   - For non-English locales: set value to `TODO: [English value]` as a placeholder.
4. **Validate**: Run JSON validation on every modified file.
5. **Report**: Show summary table with files modified, files skipped (if key already existed), any validation errors.

## Usage
```
/i18n-add key:exportBookingDate value:"Export Booking Date" after:exportBookingNo
```

## Notes
- Idempotent: safe to re-run if a key was partially inserted.
- Preserves formatting: no extra blank lines, exact indentation matching.
- Prevents duplicates: checks all locales before insertion.
