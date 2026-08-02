# FoodieBot Frontend Fix - Task Tracker

## Goal
Fix the frontend route mismatch for restaurant detail/reviews pages.

## Steps
- [x] Analyze the frontend route structure and identify the issue
- [x] Create `frontend/app/restaurant/[name]/page.tsx` (dynamic route for `/restaurant/<name>`)
- [x] Remove the stale static `frontend/app/restaurant/food` route folder
- [x] Harden params handling in the reviews page (safe decode + undefined guard)
- [x] Verify the fix by running the Next.js dev server / build

## Additional Fix: API Proxy Redirect Loop
- [x] Root cause: Next.js rewrites `/api/restaurants/` and strips the trailing slash;
      Django `APPEND_SLASH` 301-redirects back to `/api/restaurants/`, causing an
      infinite redirect loop in the browser fetch.
- [x] `frontend/next.config.ts`:
      - Added `skipTrailingSlashRedirect: true` to stop Next.js from 308-redirecting
        the trailing-slash URL before the rewrite proxy can handle it.
      - Changed rewrite destination to `http://127.0.0.1:8000/api/:path*/` (trailing
        slash preserved) so Django receives the exact path and does not need to
        APPEND_SLASH.
- [x] Verified:
      - `GET /api/restaurants/` -> 200, 4 restaurants via proxy
      - `GET /api/restaurants/<name>/reviews/` -> 200 with stats/reviews via proxy

