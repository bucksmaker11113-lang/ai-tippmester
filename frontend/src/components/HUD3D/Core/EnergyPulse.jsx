import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

export default function EnergyPulse() {
  const ring = useRef();

  useFrame((state) => {
    const t = (state.clock.getElapsedTime() % 1);

    const scale = 1 + t * 3;
    ring.current.scale.set(scale, scale, scale);
    ring.current.material.opacity = 0.4 - t * 0.4;
  });

  return (
    <mesh ref={ring} rotation={[-Math.PI / 2, 0, 0]}>
      <ringGeometry args={[0.3, 0.32, 128]} />
      <meshBasicMaterial
        color={"#00eaff"}
        transparent
        opacity={0.4}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}
