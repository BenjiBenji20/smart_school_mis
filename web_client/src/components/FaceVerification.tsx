/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useRef, useState, useEffect } from "react";

const FaceVerification: React.FC = () => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);

    const [stream, setStream] = useState<MediaStream | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [result, setResult] = useState<any>(null);

    // 🎥 Start camera
    const startCamera = async () => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 },
            });

            if (videoRef.current) {
                videoRef.current.srcObject = mediaStream;
            }

            setStream(mediaStream);
        } catch {
            setError("Camera access denied");
        }
    };

    // 🛑 Stop camera
    const stopCamera = () => {
        stream?.getTracks().forEach((track) => track.stop());
        setStream(null);
    };

    // 📸 Capture & verify
    const captureAndVerify = async () => {
        if (!videoRef.current || !canvasRef.current) return;

        setLoading(true);
        setError("");
        setResult(null);

        const video = videoRef.current;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");

        if (!ctx) return;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0);

        const imageBase64 = canvas.toDataURL("image/jpeg", 0.95);

        try {
            const res = await api.post("/face-recognition/verify", {
                image_base64: imageBase64,
                action: "test_action", // REQUIRED by backend
            });

            setResult(res.data);
            stopCamera();
        } catch (err: any) {
            setError(err.response?.data?.detail || "Verification failed");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        startCamera();
        return () => stopCamera();
        // eslint-disable-next-line
    }, []);

    return (
        <div className="flex flex-col items-center gap-4 p-6">
            <h2 className="text-xl font-bold">Face Verification</h2>

            <video
                ref={videoRef}
                autoPlay
                playsInline
                className="w-80 rounded border"
            />

            <canvas ref={canvasRef} className="hidden" />

            {error && <div className="text-red-500">{error}</div>}

            {result && (
                <pre className="bg-gray-100 p-3 rounded text-sm w-full">
                    {JSON.stringify(result, null, 2)}
                </pre>
            )}

            <button
                onClick={captureAndVerify}
                disabled={loading || !stream}
                className="px-4 py-2 bg-blue-600 text-white rounded"
            >
                {loading ? "Verifying..." : "Capture & Verify"}
            </button>
        </div>
    );
};

export default FaceVerification;
