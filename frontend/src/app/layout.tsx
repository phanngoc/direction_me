import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'MyWay - Tìm đường riêng của bạn',
  description: 'Hệ thống đánh giá 4 chỉ số IQ, EQ, DQ, AQ và định hướng nghề nghiệp dựa trên triết lý Ikigai',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="vi">
      <body className={inter.className}>{children}</body>
    </html>
  )
}