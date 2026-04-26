"use client";

import { useEffect, useRef, useState } from "react";

interface QRCodeProps {
  data: string;
  size?: number;
  title?: string;
}

export default function QRCode({ data, size = 200, title }: QRCodeProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!data || !canvasRef.current) return;

    setIsLoading(true);
    setError(null);

    // Dynamically import qrcode library
    import("qrcode").then((QRCodeLib) => {
      QRCodeLib.toCanvas(
        canvasRef.current,
        data,
        {
          width: size,
          margin: 2,
          color: {
            dark: "#000000",
            light: "#ffffff",
          },
        },
        (err: Error | null | undefined) => {
          if (err) {
            setError("Falha ao gerar QR Code");
            console.error("QR Code generation error:", err);
          } else {
            setIsLoading(false);
          }
        }
      );
    }).catch(() => {
      // Fallback: render a simple placeholder if qrcode library is not available
      setError(null);
      setIsLoading(false);
    });
  }, [data, size]);

  if (error) {
    return (
      <div className="flex flex-col items-center p-4">
        <div className="w-[200px] h-[200px] bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center border">
          <div className="text-center p-4">
            <div className="text-4xl mb-2">📱</div>
            <p className="text-xs text-muted-foreground">QR Code</p>
            <p className="text-xs text-muted-foreground break-all mt-1">{data?.substring(0, 30)}...</p>
          </div>
        </div>
        {title && <p className="text-sm font-medium mt-2">{title}</p>}
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center p-4">
      <canvas ref={canvasRef} width={size} height={size} className="rounded-lg" />
      {isLoading && (
        <div className="mt-2 text-xs text-muted-foreground">Gerando QR Code...</div>
      )}
      {title && <p className="text-sm font-medium mt-2">{title}</p>}
    </div>
  );
}
