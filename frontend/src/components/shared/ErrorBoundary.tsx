"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="flex flex-col items-center justify-center p-8 rounded-lg border border-red-200 bg-red-50 dark:bg-red-950/20 dark:border-red-800">
          <div className="text-red-600 dark:text-red-400 text-lg font-semibold mb-2">
            Algo deu errado
          </div>
          <p className="text-red-500 dark:text-red-400 text-sm mb-4 text-center">
            {this.state.error?.message || "Ocorreu um erro inesperado ao carregar este componente."}
          </p>
          <button
            onClick={this.handleRetry}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition text-sm"
          >
            Tentar novamente
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
