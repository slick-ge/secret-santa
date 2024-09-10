/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ["geist"],
};

export default nextConfig;

module.exports = {
  output: 'standalone',
};
