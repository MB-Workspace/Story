/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    async rewrites() {
        return [
            {
                source: '/api/vajra/:path*',
                destination: 'http://localhost:8000/api/vajra/:path*',
            },
        ]
    },
}

module.exports = nextConfig