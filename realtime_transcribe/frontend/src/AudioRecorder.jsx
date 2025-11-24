import React, { useState } from "react";

function AudioRecorder() {
    const [ws, setWs] = useState(null);
    let mediaRecorder;
    let audioContext;
    let processor;
    let source;

    const startRecording = async () => {
        // Connexion WebSocket
        const socket = new WebSocket("ws://127.0.0.1:8000/ws/transcribe");
        socket.binaryType = "arraybuffer";

        socket.onopen = () => {
            console.log("WS CONNECTED");
            setWs(socket);
        };

        socket.onmessage = (event) => {
            console.log("TRANSCRIPTION:", event.data);
        };

        socket.onerror = (err) => {
            console.error("WS ERROR:", err);
        };

        socket.onclose = () => {
            console.log("WS CLOSED");
        };

        // Capture micro
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
        source = audioContext.createMediaStreamSource(stream);
        processor = audioContext.createScriptProcessor(4096, 1, 1);

        processor.onaudioprocess = (e) => {
            const inputData = e.inputBuffer.getChannelData(0);
            const buffer = convertFloat32ToInt16(inputData);
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(buffer);
            }
        };

        source.connect(processor);
        processor.connect(audioContext.destination);
    };

    const stopRecording = () => {
        if (processor) processor.disconnect();
        if (source) source.disconnect();
        if (audioContext) audioContext.close();
        if (ws) ws.close();
        console.log("STOP RECORDING");
    };

    // Convertir Float32Array en PCM16
    const convertFloat32ToInt16 = (buffer) => {
        let l = buffer.length;
        const result = new Int16Array(l);
        while (l--) {
            result[l] = Math.max(-1, Math.min(1, buffer[l])) * 0x7fff;
        }
        return result.buffer;
    };

    return (
        <div>
            <button onClick={startRecording}>Démarrer</button>
            <button onClick={stopRecording}>Arrêter</button>
        </div>
    );
}

export default AudioRecorder;
