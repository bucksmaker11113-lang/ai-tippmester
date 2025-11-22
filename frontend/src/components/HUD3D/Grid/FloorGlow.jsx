import { useRef } from "react";
import * as THREE from "three";
import { useFrame } from "@react-three/fiber";

export default function FloorGlow() {
  const glow = useRef();

  useFrame((state) => {
    const t = state.clock.getElapsedTime();
    glow.current.material.opacity = 0.25 + Math.sin(t * 2) * 0.1;
  });

  return (
    <mesh
      position={[0, -1.25, 0]}
      rotation={[-Math.PI / 2, 0, 0]}
      ref={glow}
    >
      <circleGeometry args={[10, 64]} />
      <meshBasicMaterial
        color={"#0dd4ff"}
        transparent
        opacity={0.25}
        blending={THREE.AdditiveBlending}
      />
    </mesh>
  );
}
