import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            MyWay
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            Tìm đường riêng của bạn
          </p>
          <p className="text-lg text-gray-500 mb-12 max-w-2xl mx-auto">
            Hệ thống đánh giá 4 chỉ số IQ, EQ, DQ, AQ và định hướng nghề nghiệp 
            dựa trên triết lý Ikigai cho học sinh-sinh viên.
          </p>
          
          <div className="space-y-4">
            <Link 
              href="/assessment"
              className="inline-block bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Bắt đầu đánh giá
            </Link>
            
            <div className="text-sm text-gray-500">
              <p>Miễn phí • Mất khoảng 15 phút • Kết quả ngay lập tức</p>
            </div>
          </div>
        </div>
        
        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">Đánh giá 4 chỉ số</h3>
            <p className="text-gray-600">
              Kiểm tra IQ, EQ, DQ, AQ để hiểu rõ năng lực bản thân
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">Phân tích Ikigai</h3>
            <p className="text-gray-600">
              Tìm hiểu vùng giao thoa giữa đam mê, tài năng, nhu cầu xã hội và thu nhập
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">Lộ trình học tập</h3>
            <p className="text-gray-600">
              Nhận gợi ý nghề nghiệp và lộ trình phát triển cá nhân hóa
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}