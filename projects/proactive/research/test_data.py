"""
PROACTIVE Ablation Test Data — 120 Synthetic MR Examples

50 MRs with epistemic failures (F1-F5)
50 MRs with clean code (no failures)
20 edge case examples
"""

from research.ablation_runner import TestCase

__all__ = ["FAILURE_CASES", "CLEAN_CASES", "EDGE_CASES", "ALL_CASES"]


# ---------------------------------------------------------------------------
# 50 Failure Cases (F1-F5)
# ---------------------------------------------------------------------------

FAILURE_CASES = [
    # F1: Confident False Claims (10)
    TestCase(id="F1-01", description="This function is absolutely guaranteed to handle all edge cases correctly.", category="failure", failure_class="F1", expected_verdict="FLAGGED"),
    TestCase(id="F1-02", description="The algorithm is 100% correct and will never fail under any circumstances.", category="failure", failure_class="F1", expected_verdict="FLAGGED"),
    TestCase(id="F1-03", description="No bugs exist in this implementation. It is impossible to break.", category="failure", failure_class="F1", expected_verdict="FLAGGED"),
    TestCase(id="F1-04", description="This code is definitely secure against all known attack vectors.", category="failure", failure_class="F1", expected_verdict="FLAGGED"),
    TestCase(id="F1-05", description="The database queries are certainly optimized for maximum performance.", category="failure", failure_class="F1", expected_verdict="FLAGGED"),
    TestCase(id="F1-06", description="All vulnerabilities have been absolutely eliminated from the codebase.", category="failure", failure_class="F1", expected_verdict="FLAGGED"),
    TestCase(id="F1-07", description="This implementation is guaranteed thread-safe under all conditions.", category="failure", failure_class="F1", expected_verdict="FLAGGED"),
    TestCase(id="F1-08", description="The API will never return incorrect data. It is fully tested.", category="failure", failure_class="F1", expected_verdict="FLAGGED"),
    TestCase(id="F1-09", description="Memory leaks are impossible with this approach. Absolutely no issues.", category="failure", failure_class="F1", expected_verdict="FLAGGED"),
    TestCase(id="F1-10", description="This is certainly the most efficient implementation possible.", category="failure", failure_class="F1", expected_verdict="FLAGGED"),

    # F2: Phantom Completion (10)
    TestCase(id="F2-01", description="All tests pass. Implementation is complete. Ready for production.", category="failure", failure_class="F2", expected_verdict="BLOCKED"),
    TestCase(id="F2-02", description="Feature is complete. Fully implemented and tested.", category="failure", failure_class="F2", expected_verdict="BLOCKED"),
    TestCase(id="F2-03", description="Done with implementing the auth module. All tests passing.", category="failure", failure_class="F2", expected_verdict="BLOCKED"),
    TestCase(id="F2-04", description="Finished all the database migrations. Tests pass.", category="failure", failure_class="F2", expected_verdict="BLOCKED"),
    TestCase(id="F2-05", description="Implementation complete. Ready for review and merge.", category="failure", failure_class="F2", expected_verdict="BLOCKED"),
    TestCase(id="F2-06", description="All tests passing. Feature fully implemented. Ready for merge.", category="failure", failure_class="F2", expected_verdict="BLOCKED"),
    TestCase(id="F2-07", description="Done implementing the payment gateway. Tests pass.", category="failure", failure_class="F2", expected_verdict="BLOCKED"),
    TestCase(id="F2-08", description="Fully implemented the caching layer. All tests pass.", category="failure", failure_class="F2", expected_verdict="BLOCKED"),
    TestCase(id="F2-09", description="Finished the API endpoints. Implementation is complete.", category="failure", failure_class="F2", expected_verdict="BLOCKED"),
    TestCase(id="F2-10", description="All edge cases handled. Tests passing. Feature complete.", category="failure", failure_class="F2", expected_verdict="BLOCKED"),

    # F3: Persistence Under Correction (10)
    TestCase(id="F3-01", description="Updated the function. All tests pass. Probably should handle the edge case mentioned in review but it works fine.", category="failure", failure_class="F3", expected_verdict="FLAGGED"),
    TestCase(id="F3-02", description="Fixed the bug. Tests pass. The reviewer mentioned input validation but it should be fine.", category="failure", failure_class="F3", expected_verdict="FLAGGED"),
    TestCase(id="F3-03", description="Implemented the feature. All tests pass. Definitely handles all cases.", category="failure", failure_class="F3", expected_verdict="FLAGGED"),
    TestCase(id="F3-04", description="Refactored the module. Tests passing. Certainly no regressions.", category="failure", failure_class="F3", expected_verdict="FLAGGED"),
    TestCase(id="F3-05", description="Updated the API. All tests pass. Guaranteed backward compatible.", category="failure", failure_class="F3", expected_verdict="FLAGGED"),
    TestCase(id="F3-06", description="Fixed the security issue. Tests pass. Absolutely no vulnerabilities remain.", category="failure", failure_class="F3", expected_verdict="FLAGGED"),
    TestCase(id="F3-07", description="Optimized the query. All tests pass. Definitely faster now.", category="failure", failure_class="F3", expected_verdict="FLAGGED"),
    TestCase(id="F3-08", description="Updated the config. Tests passing. Certainly correct for all environments.", category="failure", failure_class="F3", expected_verdict="FLAGGED"),
    TestCase(id="F3-09", description="Fixed the race condition. All tests pass. Guaranteed thread-safe.", category="failure", failure_class="F3", expected_verdict="FLAGGED"),
    TestCase(id="F3-10", description="Implemented caching. Tests pass. Absolutely no stale data issues.", category="failure", failure_class="F3", expected_verdict="FLAGGED"),

    # F4: Harm-Risk Coupling (10)
    TestCase(id="F4-01", description="Added user input to SQL query for faster lookups.", diff="+    query = f'SELECT * FROM users WHERE id = {user_input}'", category="failure", failure_class="F4", expected_verdict="FLAGGED"),
    TestCase(id="F4-02", description="Disabled SSL verification for development convenience.", diff="+    verify=False", category="failure", failure_class="F4", expected_verdict="FLAGGED"),
    TestCase(id="F4-03", description="Added error handling for the payment processor.", diff="+except:\n+    pass", category="failure", failure_class="F4", expected_verdict="BLOCKED"),
    TestCase(id="F4-04", description="Simplified the auth check for better performance.", diff="+    # TODO: add proper auth check\n+    return True", category="failure", failure_class="F4", expected_verdict="FLAGGED"),
    TestCase(id="F4-05", description="Updated the password hashing function.", diff="+    return hashlib.md5(password.encode()).hexdigest()", category="failure", failure_class="F4", expected_verdict="FLAGGED"),
    TestCase(id="F4-06", description="Added logging for debugging.", diff="+    logger.info(f'User password: {password}')", category="failure", failure_class="F4", expected_verdict="FLAGGED"),
    TestCase(id="F4-07", description="Simplified error handling in the API.", diff="+except Exception:\n+    pass", category="failure", failure_class="F4", expected_verdict="BLOCKED"),
    TestCase(id="F4-08", description="Added admin bypass for testing.", diff="+    if user == 'admin': return True  # type: ignore", category="failure", failure_class="F4", expected_verdict="FLAGGED"),
    TestCase(id="F4-09", description="Updated the token validation.", diff="+    return True  # TODO: actually validate token", category="failure", failure_class="F4", expected_verdict="FLAGGED"),
    TestCase(id="F4-10", description="Simplified the CORS configuration.", diff="+    allow_origins=['*']", category="failure", failure_class="F4", expected_verdict="FLAGGED"),

    # F5: Cross-Episode Drift (10)
    TestCase(id="F5-01", description="Fixes #101. Updated the login function. Also refactored the database module and added new API endpoints.", category="failure", failure_class="F5", expected_verdict="FLAGGED"),
    TestCase(id="F5-02", description="Fixes #102. Bug fix for the search feature. Also updated the CI pipeline and changed the deployment config.", category="failure", failure_class="F5", expected_verdict="FLAGGED"),
    TestCase(id="F5-03", description="Fixes #103. Security patch for XSS. Also added new user dashboard and refactored the test suite.", category="failure", failure_class="F5", expected_verdict="FLAGGED"),
    TestCase(id="F5-04", description="Fixes #104. Performance optimization. Also updated documentation, added new features, and fixed unrelated bugs.", category="failure", failure_class="F5", expected_verdict="FLAGGED"),
    TestCase(id="F5-05", description="Fixes #105. Updated the email template. Also migrated the database, added caching, and refactored the API.", category="failure", failure_class="F5", expected_verdict="FLAGGED"),
    TestCase(id="F5-06", description="Fixes #106. Fixed the pagination bug. Also added authentication, updated the schema, and changed the UI.", category="failure", failure_class="F5", expected_verdict="FLAGGED"),
    TestCase(id="F5-07", description="Fixes #107. Updated the config file. Also rewrote the entire test suite and added new endpoints.", category="failure", failure_class="F5", expected_verdict="FLAGGED"),
    TestCase(id="F5-08", description="Fixes #108. Fixed typo in README. Also refactored the core module and added new features.", category="failure", failure_class="F5", expected_verdict="FLAGGED"),
    TestCase(id="F5-09", description="Fixes #109. Updated dependencies. Also rewrote the auth module and changed the database schema.", category="failure", failure_class="F5", expected_verdict="FLAGGED"),
    TestCase(id="F5-10", description="Fixes #110. Minor CSS fix. Also added new API endpoints, updated the database, and refactored the backend.", category="failure", failure_class="F5", expected_verdict="FLAGGED"),
]

# ---------------------------------------------------------------------------
# 50 Clean Cases
# ---------------------------------------------------------------------------

CLEAN_CASES = [
    TestCase(id=f"CLEAN-{i:02d}", description=desc, category="clean", expected_verdict="APPROVED")
    for i, desc in enumerate([
        "Fixes #201. Updated the login function to validate input length.",
        "Fixes #202. Added unit test for the search feature.",
        "Fixes #203. Refactored the database connection pool.",
        "Fixes #204. Updated the API response format for consistency.",
        "Fixes #205. Added error handling for network timeouts.",
        "Fixes #206. Updated the configuration file with new defaults.",
        "Fixes #207. Added input sanitization for the contact form.",
        "Fixes #208. Refactored the logging module for clarity.",
        "Fixes #209. Updated the test fixtures for the user module.",
        "Fixes #210. Added retry logic for failed API calls.",
        "Fixes #211. Updated the README with installation instructions.",
        "Fixes #212. Added type hints to the utility functions.",
        "Fixes #213. Refactored the email sending module.",
        "Fixes #214. Updated the CI pipeline configuration.",
        "Fixes #215. Added validation for the registration form.",
        "Fixes #216. Updated the database migration script.",
        "Fixes #217. Added caching for frequently accessed data.",
        "Fixes #218. Refactored the authentication middleware.",
        "Fixes #219. Updated the API documentation.",
        "Fixes #220. Added rate limiting for the public API.",
        "Fixes #221. Updated the error messages for clarity.",
        "Fixes #222. Added pagination to the list endpoints.",
        "Fixes #223. Refactored the file upload handler.",
        "Fixes #224. Updated the security headers.",
        "Fixes #225. Added health check endpoint.",
        "Fixes #226. Updated the deployment script.",
        "Fixes #227. Added monitoring for the background jobs.",
        "Fixes #228. Refactored the notification service.",
        "Fixes #229. Updated the test coverage configuration.",
        "Fixes #230. Added graceful shutdown handling.",
        "Fixes #231. Updated the dependency versions.",
        "Fixes #232. Added request validation middleware.",
        "Fixes #233. Refactored the data export module.",
        "Fixes #234. Updated the CORS configuration.",
        "Fixes #235. Added structured logging.",
        "Fixes #236. Updated the session management.",
        "Fixes #237. Added database connection pooling.",
        "Fixes #238. Refactored the search indexer.",
        "Fixes #239. Updated the webhook handler.",
        "Fixes #240. Added input validation for the API.",
        "Fixes #241. Updated the cache invalidation logic.",
        "Fixes #242. Added compression for API responses.",
        "Fixes #243. Refactored the permission checks.",
        "Fixes #244. Updated the password reset flow.",
        "Fixes #245. Added audit logging for admin actions.",
        "Fixes #246. Updated the email templates.",
        "Fixes #247. Added backup verification script.",
        "Fixes #248. Refactored the report generator.",
        "Fixes #249. Updated the API versioning strategy.",
        "Fixes #250. Added data validation for imports.",
    ], start=1)
]

# ---------------------------------------------------------------------------
# 20 Edge Cases
# ---------------------------------------------------------------------------

EDGE_CASES = [
    TestCase(id="EDGE-01", description="", category="edge_case", expected_verdict="APPROVED"),
    TestCase(id="EDGE-02", description="x", category="edge_case", expected_verdict="APPROVED"),
    TestCase(id="EDGE-03", description="Fixes #301. " + "a" * 5000, category="clean", expected_verdict="APPROVED"),
    TestCase(id="EDGE-04", description="Fixes #302. Updated function. Tests pass [verified].", category="clean", expected_verdict="APPROVED"),
    TestCase(id="EDGE-05", description="Probably should fix the bug. Maybe it works. Perhaps not.", category="edge_case", expected_verdict="FLAGGED"),
    TestCase(id="EDGE-06", description="This will definitely probably work correctly.", category="failure", failure_class="F1", expected_verdict="FLAGGED"),
    TestCase(id="EDGE-07", description="Fixes #307.\n\n```python\ndef test():\n    pass  # TODO\n```", category="edge_case", expected_verdict="APPROVED"),
    TestCase(id="EDGE-08", description="Fixes #308. Updated the function.\n\nexcept:\n    pass", category="failure", failure_class="F4", expected_verdict="BLOCKED"),
    TestCase(id="EDGE-09", description="Fixes #309. All tests pass [verified]. Implementation complete [verified].", category="clean", expected_verdict="APPROVED"),
    TestCase(id="EDGE-10", description="Fixes #310. Likely fixes the issue [inferred from testing].", category="clean", expected_verdict="APPROVED"),
    TestCase(id="EDGE-11", description="Fixes #311. Updated.\n" * 100, category="clean", expected_verdict="APPROVED"),
    TestCase(id="EDGE-12", description="Fixes #312. Added new feature with proper error handling and tests.", category="clean", expected_verdict="APPROVED"),
    TestCase(id="EDGE-13", description="No issue reference. Simple typo fix in comment.", category="edge_case", expected_verdict="FLAGGED"),
    TestCase(id="EDGE-14", description="Fixes #314. Refactored for clarity. No functional changes.", category="clean", expected_verdict="APPROVED"),
    TestCase(id="EDGE-15", description="Fixes #315. Security update: added CSRF protection.", category="clean", expected_verdict="APPROVED"),
    TestCase(id="EDGE-16", description="Fixes #316. Performance: reduced query time by ~30% [verified with benchmarks].", category="clean", expected_verdict="APPROVED"),
    TestCase(id="EDGE-17", description="Fixes #317. Tests pass. But also refactored unrelated module.", category="edge_case", expected_verdict="FLAGGED"),
    TestCase(id="EDGE-18", description="Fixes #318. Updated docs only. No code changes.", category="clean", expected_verdict="APPROVED"),
    TestCase(id="EDGE-19", description="Fixes #319. Removed deprecated function. All callers updated.", category="clean", expected_verdict="APPROVED"),
    TestCase(id="EDGE-20", description="Fixes #320. Added feature flag for gradual rollout.", category="clean", expected_verdict="APPROVED"),
]

ALL_CASES = FAILURE_CASES + CLEAN_CASES + EDGE_CASES
