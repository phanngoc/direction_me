/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': require('path').resolve(__dirname, 'src'),
      '@/components': require('path').resolve(__dirname, 'src/components'),
      '@/pages': require('path').resolve(__dirname, 'src/pages'),
      '@/utils': require('path').resolve(__dirname, 'src/utils'),
      '@/services': require('path').resolve(__dirname, 'src/services'),
      '@/hooks': require('path').resolve(__dirname, 'src/hooks'),
      '@/shared': require('path').resolve(__dirname, '../shared'),
    };
    return config;
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL 
          ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`
          : 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
