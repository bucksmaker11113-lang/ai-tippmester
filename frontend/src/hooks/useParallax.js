import { useState } from "react";

export function useParallax(maxTilt = 8) {
    const [style, setStyle] = useState({});

    function move(e) {
        const rect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const dx = ((x - centerX) / centerX) * maxTilt;
        const dy = ((y - centerY) / centerY) * -maxTilt;

        setStyle({ transform: `perspective(900px) rotateX(${dy}deg) rotateY(${dx}deg)` });
    }

    function reset() {
        setStyle({ transform: "perspective(900px) rotateX(0deg) rotateY(0deg)" });
    }

    return { style, move, reset };
}
