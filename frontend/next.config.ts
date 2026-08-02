import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Disable Next.js auto trailing-slash redirects so /api/... proxied
  // requests reach Django unchanged (Django's APPEND_SLASH adds the
  // trailing slash, which previously created a 308 <-> 301 redirect loop).
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return [
      {
        // Proxy all /api/* requests to the Django backend (same-origin, no CORS needed)
        // The trailing "/" on the destination is required: Next.js strips the
        // trailing slash from the :path* capture, which would otherwise make
        // Django's APPEND_SLASH 301-redirect in a loop.
        source: "/api/:path*",
        destination: "http://127.0.0.1:8000/api/:path*/",
      },
    ];
  },
};

export default nextConfig;
