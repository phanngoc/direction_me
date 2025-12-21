'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { validateEmail, validatePassword, validateAge, setToStorage, STORAGE_KEYS } from '@/utils/helpers';

interface RegisterFormData {
  email: string;
  password: string;
  full_name: string;
  age: number;
}

interface RegisterResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    email: string;
    full_name: string;
    age: number;
    created_at: string;
    updated_at: string;
  };
}

export default function RegisterPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [formData, setFormData] = useState<RegisterFormData>({
    email: '',
    password: '',
    full_name: '',
    age: 20
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Partial<RegisterFormData>>({});

  // Get redirect URL from query params
  const redirectTo = searchParams.get('redirect') || '/assessment';

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
    if (token) {
      router.push(redirectTo);
    }
  }, [router, redirectTo]);

  const validateForm = (): boolean => {
    const errors: Partial<RegisterFormData> = {};
    
    if (!formData.email) {
      errors.email = 'Email là bắt buộc';
    } else if (!validateEmail(formData.email)) {
      errors.email = 'Email không hợp lệ';
    }
    
    if (!formData.password) {
      errors.password = 'Mật khẩu là bắt buộc';
    } else if (!validatePassword(formData.password)) {
      errors.password = 'Mật khẩu phải có 8-24 ký tự và bao gồm cả chữ và số';
    }
    
    if (!formData.full_name.trim()) {
      errors.full_name = 'Họ tên là bắt buộc';
    }
    
    if (!formData.age) {
      errors.age = 'Tuổi là bắt buộc';
    } else if (!validateAge(formData.age)) {
      errors.age = 'Tuổi phải từ 16 đến 25';
    }
    
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;
    const newValue = type === 'number' ? parseInt(value) || 0 : value;
    
    setFormData(prev => ({ ...prev, [name]: newValue }));
    
    // Clear field error when user starts typing
    if (fieldErrors[name as keyof RegisterFormData]) {
      setFieldErrors(prev => ({ ...prev, [name]: undefined }));
    }
    
    // Clear general error
    if (error) {
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 400) {
          if (data.detail && data.detail.includes('email')) {
            setError('Email này đã được sử dụng');
          } else {
            setError(data.detail || 'Dữ liệu không hợp lệ');
          }
        } else if (response.status === 422) {
          setError('Dữ liệu không hợp lệ');
        } else {
          setError(data.detail || 'Đã xảy ra lỗi không xác định');
        }
        return;
      }

      // Save token and user data
      setToStorage(STORAGE_KEYS.ACCESS_TOKEN, data.access_token);
      setToStorage(STORAGE_KEYS.USER_DATA, data.user);

      // Redirect to intended page
      router.push(redirectTo);
    } catch (err) {
      console.error('Register error:', err);
      setError('Không thể kết nối đến server. Vui lòng thử lại sau.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold text-gray-900">
            Đăng ký tài khoản
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Hoặc{' '}
            <Link
              href={`/login${redirectTo !== '/assessment' ? `?redirect=${encodeURIComponent(redirectTo)}` : ''}`}
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              đăng nhập với tài khoản có sẵn
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm">{error}</p>
                </div>
              </div>
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="label">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={formData.email}
                onChange={handleInputChange}
                className={`input ${fieldErrors.email ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                placeholder="Nhập email của bạn"
              />
              {fieldErrors.email && (
                <p className="mt-1 text-sm text-red-600">{fieldErrors.email}</p>
              )}
            </div>

            <div>
              <label htmlFor="password" className="label">
                Mật khẩu
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                value={formData.password}
                onChange={handleInputChange}
                className={`input ${fieldErrors.password ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                placeholder="8-24 ký tự, bao gồm chữ và số"
              />
              {fieldErrors.password && (
                <p className="mt-1 text-sm text-red-600">{fieldErrors.password}</p>
              )}
            </div>

            <div>
              <label htmlFor="full_name" className="label">
                Họ và tên
              </label>
              <input
                id="full_name"
                name="full_name"
                type="text"
                autoComplete="name"
                required
                value={formData.full_name}
                onChange={handleInputChange}
                className={`input ${fieldErrors.full_name ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                placeholder="Nhập họ và tên đầy đủ"
              />
              {fieldErrors.full_name && (
                <p className="mt-1 text-sm text-red-600">{fieldErrors.full_name}</p>
              )}
            </div>

            <div>
              <label htmlFor="age" className="label">
                Tuổi
              </label>
              <input
                id="age"
                name="age"
                type="number"
                min="16"
                max="25"
                required
                value={formData.age}
                onChange={handleInputChange}
                className={`input ${fieldErrors.age ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                placeholder="16-25"
              />
              {fieldErrors.age && (
                <p className="mt-1 text-sm text-red-600">{fieldErrors.age}</p>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full flex justify-center py-3"
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Đang tạo tài khoản...
                </>
              ) : (
                'Tạo tài khoản'
              )}
            </button>
          </div>

          <div className="text-center">
            <Link
              href="/"
              className="text-sm text-gray-600 hover:text-gray-500"
            >
              ← Về trang chủ
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
