'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('ErrorBoundary caught an error:', error, errorInfo);
    }

    // Call custom error handler if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // Update state with error info
    this.setState({ error, errorInfo });

    // Log to external service in production
    if (process.env.NODE_ENV === 'production') {
      // Here you would typically send the error to a logging service
      // like Sentry, LogRocket, etc.
      console.error('Production error:', error, errorInfo);
    }
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
  };

  render() {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default fallback UI
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6 text-center">
            <div className="text-red-600 text-6xl mb-4">⚠️</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Đã xảy ra lỗi
            </h2>
            <p className="text-gray-600 mb-6">
              Xin lỗi, đã có lỗi không mong muốn xảy ra. Vui lòng thử lại.
            </p>
            
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <details className="mb-4 text-left">
                <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700">
                  Chi tiết lỗi (Development)
                </summary>
                <div className="mt-2 p-3 bg-gray-100 rounded text-xs font-mono text-red-600 overflow-auto">
                  <div><strong>Error:</strong> {this.state.error.message}</div>
                  <div><strong>Stack:</strong></div>
                  <pre className="whitespace-pre-wrap">{this.state.error.stack}</pre>
                  {this.state.errorInfo && (
                    <>
                      <div><strong>Component Stack:</strong></div>
                      <pre className="whitespace-pre-wrap">{this.state.errorInfo.componentStack}</pre>
                    </>
                  )}
                </div>
              </details>
            )}
            
            <div className="space-y-3">
              <button
                onClick={this.handleRetry}
                className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Thử lại
              </button>
              <button
                onClick={() => window.location.href = '/'}
                className="w-full bg-gray-200 text-gray-800 px-4 py-2 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
              >
                Về trang chủ
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// Higher-order component for easier usage
export function withErrorBoundary<P extends object>(
  Component: React.ComponentType<P>,
  errorBoundaryProps?: Omit<Props, 'children'>
) {
  return function WithErrorBoundaryComponent(props: P) {
    return (
      <ErrorBoundary {...errorBoundaryProps}>
        <Component {...props} />
      </ErrorBoundary>
    );
  };
}

// Hook for functional components to trigger error boundary
export function useErrorHandler() {
  return (error: Error, errorInfo?: ErrorInfo) => {
    // This will trigger the error boundary
    throw error;
  };
}

// Utility function to log errors
export function logError(error: Error, errorInfo?: ErrorInfo, context?: string) {
  const errorData = {
    message: error.message,
    stack: error.stack,
    componentStack: errorInfo?.componentStack,
    context,
    timestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    url: window.location.href,
  };

  // Log to console in development
  if (process.env.NODE_ENV === 'development') {
    console.error('Error logged:', errorData);
  }

  // In production, you would send this to your error tracking service
  if (process.env.NODE_ENV === 'production') {
    // Example: send to Sentry, LogRocket, etc.
    console.error('Production error logged:', errorData);
  }
}