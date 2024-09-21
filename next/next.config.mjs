/** @type {import('next').NextConfig} */
const nextConfig = {
    rewrites: async () => {
      return [
        {
          source: '/flask/:path*',
          destination:
            process.env.NODE_ENV === 'development'
              ? 'http://127.0.0.1:5328/flask/:path*'
              : '/flask/',
        },
      ]
   },
}
  
export default nextConfig;
