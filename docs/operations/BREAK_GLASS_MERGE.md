# SOP: Administrative Ruleset Bypass
If CI status checks (e.g., fde-crsp-verify) fail due to structural refactoring:
1. Go to [TLC-main-governance Ruleset](https://github.com/coreyalejandro/the-living-constitution/settings/rules/14711975).
2. Uncheck "Require status checks to pass before merging".
3. Uncheck "Require a pull request before merging".
4. Save Changes.
5. Execute: git push origin main --force
6. Re-enable rules after successful push.
