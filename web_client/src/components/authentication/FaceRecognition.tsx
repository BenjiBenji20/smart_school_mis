/**
 * Date Written: 1/16/2026 at 4:05 PM
 */
import { useRef, useState, useEffect } from 'react';
import { Camera, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';

interface FaceRecognitionStepProps {
    onCapture?: (imageData: string) => void;
}

export function FaceRecognitionStep({ onCapture }: FaceRecognitionStepProps) {
    const videoRef = useRef<HTMLVideoElement>(null);
    const [isCameraActive, setIsCameraActive] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const startCamera = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'user' }
            });
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                setIsCameraActive(true);
                setError(null);
            }
        } catch (err) {
            setError('Unable to access camera. Please check your permissions.');
            console.error('Camera error:', err);
        }
    };

    const stopCamera = () => {
        if (videoRef.current && videoRef.current.srcObject) {
            const stream = videoRef.current.srcObject as MediaStream;
            stream.getTracks().forEach(track => track.stop());
            setIsCameraActive(false);
        }
    };

    const captureImage = () => {
        if (videoRef.current) {
            const canvas = document.createElement('canvas');
            canvas.width = videoRef.current.videoWidth;
            canvas.height = videoRef.current.videoHeight;
            const ctx = canvas.getContext('2d');
            if (ctx) {
                ctx.drawImage(videoRef.current, 0, 0);
                const imageData = canvas.toDataURL('image/jpeg');
                onCapture?.(imageData);
            }
        }
    };

    useEffect(() => {
        return () => {
            stopCamera();
        };
    }, []);

    return (
        <div className="w-full space-y-6">
            <div className="text-center space-y-2">
                <h3 className="text-xl font-semibold">Face Recognition</h3>
                <p className="text-sm text-muted-foreground">
                    Position your face within the frame for verification
                </p>
            </div>

            {error && (
                <Alert variant="destructive">
                    <AlertDescription>{error}</AlertDescription>
                </Alert>
            )}

            <div className="relative aspect-video bg-muted rounded-lg overflow-hidden flex items-center justify-center">
                {isCameraActive ? (
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        className="w-full h-full object-cover"
                    />
                ) : (
                    <div className="text-center space-y-4">
                        <Camera className="h-16 w-16 text-muted-foreground mx-auto" />
                        <p className="text-sm text-muted-foreground">Camera is not active</p>
                    </div>
                )}
            </div>

            <div className="flex gap-3">
                {!isCameraActive ? (
                    <Button onClick={startCamera} className="flex-1">
                        <Camera className="h-4 w-4 mr-2" />
                        Start Camera
                    </Button>
                ) : (
                    <>
                        <Button onClick={captureImage} className="flex-1">
                            Capture & Verify
                        </Button>
                        <Button onClick={stopCamera} variant="outline">
                            <RefreshCw className="h-4 w-4" />
                        </Button>
                    </>
                )}
            </div>

            <p className="text-xs text-center text-muted-foreground">
                Make sure your face is well-lit and clearly visible
            </p>
        </div>
    );
}